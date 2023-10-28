import asyncio
import concurrent.futures
import datetime
import os
import threading
import traceback
from concurrent.futures import ThreadPoolExecutor

from pymilvus import (
    connections,
    utility,
    Collection,
)
from starlette.websockets import WebSocket
from transformers import LlamaForCausalLM, LlamaTokenizer, TextIteratorStreamer
from apps.chat.dependencies import SessionManager
from apps.chat.llm_task import LLMTask
from apps.chat.schemas import websocket_response_data
from apps.chat.websocket_manager import ConnectionManager
from apps.chat.ws_status import WSStatus
from utils.util import get_suid
from utils.util import format_chat_history_list, glm_format_chat_history_list, baichuan_format_chat_history_list
from apps.chat import crud

COLLECTION_NAME = os.environ.get('MILVUS_COLLECTION_NAME')  # Collection name
# DIMENSION = 768  # Embeddings size
# COUNT = 1000  # Number of vectors to insert
MILVUS_HOST = os.environ.get('MILVUS_HOST')
MILVUS_PORT = int(os.environ.get('MILVUS_PORT'))

""" 连接 Milvus """
connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
has = utility.has_collection(COLLECTION_NAME)
collection = Collection(name=COLLECTION_NAME)
collection.load()

# bert 模型地址
BERT_BASE_MODEL = os.environ.get('BERT_BASE_MODEL')

ENV = os.environ.get('ENV_PROFILE')

LLM_MODEL = os.environ.get('CHAT_MODEL')

if ENV == 'prod':
    from apps.chat import llama_loader, crud
    # from apps.chat.llama_loader import generator, LlamaModel
    from sentence_transformers import SentenceTransformer
    from apps.chat.llama_loader import transformer
    # transformer = SentenceTransformer(BERT_BASE_MODEL)
    llama_model = llama_loader.LlamaModel()
    model = llama_model.model
    instruction = llama_model.instruction
    tokenizer = llama_model.tokenizer
else:
    llama_model = {}


class TaskIdQueue(object):
    """ 后端大模型生成任务列表
        :task_id_queue key x_current_user_id, value task_id
     """

    def __init__(self):
        self.lock = threading.RLock()
        """:task_id_queue key x_current_user_id, value task_id"""
        self.task_id_queue = {}
        """key: task_id, value: LLMTask"""
        self.llm_tasks = {}
        """key: future, value:LLMTask"""
        self.future_llm_task_map = {}

    def new_task_id(self, user_id, manager: ConnectionManager, session_id, chat_history_id):
        with self.lock:
            task_id = get_suid()
            self.task_id_queue[user_id] = task_id
            self.llm_tasks[task_id] = LLMTask(task_id, user_id, manager, session_id, chat_history_id)

    def get_user_task_id(self, user_id):
        return self.task_id_queue.get(user_id)

    def get_user_llm_task(self, user_id):
        return self.llm_tasks.get(self.get_user_task_id(user_id))

    def set_user_task_future(self, user_id, future):
        task: LLMTask = self.get_user_llm_task(user_id)
        if future is not None and task is not None:
            task.set_future(future)
            with self.lock:
                self.future_llm_task_map[future] = task

    def remove_user_task(self, user_id):
        """
            remove task_id_queue immediately,
            set stopped, all task item, llm_task future will remove by background thread
        """
        if self.get_user_task_id(user_id) is not None:
            self.set_task_stopped(self.get_user_task_id(user_id))
            with self.lock:
                del self.task_id_queue[user_id]

    def set_task_stopped(self, task_id):
        if self.llm_tasks.get(task_id) is not None:
            llm_task: LLMTask = self.llm_tasks.get(task_id)
            llm_task.cancel()
            return 0
        else:
            print(f'Task id {task_id}  llm_task is not exist')
            return -1

    def remove_back_task(self, task_id):
        """
        remove back task, llm_task , future
        :param task_id:
        :return:
        """
        with self.lock:
            self.remove_future_llm_task_by_id(task_id)
            self.remove_llm_task(task_id)

    def remove_llm_task(self, task_id):
        if self.llm_tasks.get(task_id) is not None:
            with self.lock:
                llm_task = self.llm_tasks[task_id]
                del llm_task
                del self.llm_tasks[task_id]

    def remove_future_llm_task_by_id(self, task_id):
        llm_task = self.llm_tasks.get(task_id)
        if llm_task is not None:
            future = llm_task.future
            self.remove_future_llm_task_by_future(future)

    def remove_future_llm_task_by_future(self, future):
        if self.future_llm_task_map.get(future) is not None:
            with self.lock:
                del self.future_llm_task_map[future]
                print(f'delete future object:{future} done')


task_queue = TaskIdQueue()


def get_task_queue():
    return task_queue.task_id_queue


def wrap_coroutine_fn(fn, *args, **kwargs):
    return asyncio.run(fn(*args, **kwargs))


async def llm_generate_handlers(manager: ConnectionManager, websocket: WebSocket, input_data, x_current_user_id: int):
    """
    处理 总任务
    :param manager:
    :param websocket:
    :param input_data:
    :param x_current_user_id:
    :return:
    """
    mode = input_data["assistant_type"]

    if mode == "default" or mode == "engineering" or mode == "hydro" or mode == "test":
        if x_current_user_id not in task_queue.task_id_queue.keys():
            # todo 检查 session_id 和 chat_history_id 属于当前用户
            task_queue.new_task_id(x_current_user_id, manager, input_data.get("session_id"),
                                   input_data.get("chat_history_id"))
        else:
            print(f"当前用户已经有任务在运行，不能重复运行，userID:{x_current_user_id}")
            rsp = websocket_response_data(task_id=task_queue.get_user_task_id(x_current_user_id),
                                          code=WSStatus.RUNNING.value,
                                          msg=f"当前用户已经有任务在运行，不能重复运行，userID:{x_current_user_id}")
            await manager.send_json(rsp, websocket)
            return
    fn_handler = None
    if mode == "default":
        fn_handler = llm_default_handler
    elif mode == "engineering":
        fn_handler = llm_knowkdge_qa_handler
    elif mode == "hydro":
        pass
    elif mode == "test":
        fn_handler = llm_test_handler
    else:
        pass
    wrap_llm_handler_thread(fn_handler, task_queue.get_user_task_id(x_current_user_id), manager, websocket, input_data,
                            x_current_user_id)


async def llm_stop_generate_handler(manager: ConnectionManager, websocket: WebSocket, input_data,
                                    user_id: int):
    if task_queue.get_user_task_id(user_id) is not None:
        task_id = task_queue.get_user_task_id(user_id)
        print(f'开始删除, userId task_id {task_id}')
        session_id = task_queue.llm_tasks.get(task_id).session_id
        chat_history_id = task_queue.llm_tasks.get(task_id).chat_history_id
        task_queue.remove_user_task(user_id)
        rsp = websocket_response_data(task_id=task_id,
                                      code=WSStatus.STOPPED.value,
                                      session_id=session_id,
                                      chat_history_id=chat_history_id,
                                      msg=f"taskID:{task_id} 已经停止")

    else:
        msg = f'userID {user_id} task_id is not exist'
        rsp = websocket_response_data(code=WSStatus.NOT_FOUND.value, msg=msg)
        print(msg)
    await manager.send_json(rsp, websocket)


def stop_user_task(user_id):
    task_queue.remove_user_task(user_id)


def mysql_db_handler(full_output, json_data, generation_kwargs, question, input_data, task: LLMTask):
    chat_history = {"answer": full_output, "extra_info": json_data, "model_param": generation_kwargs,
                    "created_time": datetime.datetime.now(), "prompt": question,
                    "session_id": input_data["session_id"], 'likes': False, 'dislikes': False, 'comment': None,
                    'dislike_tag': [], 'comment_time': None}
    print("Here DB inserting")
    with SessionManager() as db:
        if input_data.get("chat_history_id") is not None:
            # print("*********Mysql Updating chat history")
            task.chat_history_id = crud.update_last_chat(db, chat_history).id
        else:
            # print("*********Mysql Adding chat history")
            task.chat_history_id = crud.create_dialogue(db, chat_history).id


async def llm_knowkdge_qa_handler(task: LLMTask, task_id, manager: ConnectionManager, websocket: WebSocket, input_data, user_id: int):
    question_type = '<reserved_106>' + "请判断以下问题是[生活常识问题]或是[工程专业问题]，仅回答[生活常识问题]或[工程专业问题]:" + input_data["prompt"] + '<reserved_107>'
    inputs = tokenizer.encode(question_type, return_tensors='pt').cuda()
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True, timeout=300)
    generate_ids = model.generate(inputs, streamer=streamer)
    llm_result = tokenizer.decode(generate_ids[:, len(tokenizer.encode(question_type)) :][0])
    print("Here****************" + llm_result + "*****************************")
    if "生活常识" in llm_result :
        generation_kwargs = input_data["generation_params"]
        if "chuan" in LLM_MODEL:
            question = '<reserved_106>' + input_data["prompt"] + '<reserved_107>'
        print("用户没有问知识库中问题，进入普通问答")
        llm_input = instruction.format(question)
        full_output, json_data = await llama_model.generate(task, llm_input, manager, websocket,
                                             max_length = 2048,
                                             do_sample = True,
                                             top_p = 0.7,
                                             temperature = 0.95)
        print("专业模式-普通问答 generation完成：" )
        print(full_output)
        mysql_db_handler(full_output, None, generation_kwargs, input_data["prompt"], input_data, task)
        return
    print("进入知识库")
    """知识库模式""" 
    generation_kwargs = input_data["generation_params"]
    question = input_data["prompt"]
    search_data = transformer.encode(question)
    res = collection.search(
        data=[search_data],  # Embeded search value
        anns_field="embedding",  # Search across embeddings
        param={},
        limit=3,  # Limit to top_k results per search
        output_fields=['co_id'],  # Include title field in result
    )
    json_data = []
    this_json = {}
    knowledge_base = ''
    
    # 模糊匹配关键词
    # similar_keyword = [('',0)]
    # keyword_to_item = ''
    # with open .json:
    #     for data in keyword_json:
    #         temp_similar_keyword = process.extract(question, data['keywords'], limit=1)
    #         if temp_similar_keyword[0][1]>similar_keyword[0][1]:
    #             similar_keyword = temp_similar_keyword
    #             keyword_to_item = data['content']
    #             this_json = data
    # json_data.append(this_json)
    # this_json = {}
    # if keyword_to_item not in knowledge_base:
    #     knowledge_base += keyword_to_item
    print(res)
    with SessionManager() as db:
        for hits_i, hits in enumerate(res):
            for i, hit in enumerate(hits):
                co_id = hit.entity.get('co_id')
                fetch_provision_detail = crud.get_provision_by_co_id(db, co_id)
                this_json['doc_id'] = str(fetch_provision_detail.doc_id)
                this_json['content'] = str(fetch_provision_detail.content)
                this_json['page'] = int(fetch_provision_detail.page)
                this_json['doc_name'] = str(fetch_provision_detail.doc_name)
                this_json['key_word'] = str(fetch_provision_detail.key_word)
                this_json['title'] = str(fetch_provision_detail.title)
                
                knowledge_base = knowledge_base + '## 条文' + str(i+1) + str(fetch_provision_detail.content)
                knowledge_base += '\n\n'
                json_data.append(this_json)
                this_json = {}
    json_data = list(set([tuple(d.items()) for d in json_data]))
    json_data = [dict(t) for t in json_data]
   
    llm_input = instruction.format("请参考下列条文之一回答最后的问题，如果问题不能在条文中找到答案，请回复“对不起，我无法找到相关的规定”:\n\n" 
                                   + knowledge_base + "\n## 问题:" +question + "\n\n## 答:\n")
    
    if "chuan" in LLM_MODEL:
            llm_input = '<reserved_106>' + llm_input + '<reserved_107>'
    print(llm_input)
    print(json_data)
    full_output, json_data = await llama_model.generate(task, llm_input, manager, websocket, json_data,
                                            max_length=generation_kwargs["max_length"] if generation_kwargs[
                                                 "max_length"] else 2048,
                                             do_sample=True,
                                             top_p=generation_kwargs["top_p"] if generation_kwargs[
                                                 "top_p"] else 0.85,
                                             temperature=generation_kwargs["temperature"] if generation_kwargs[
                                                 "temperature"] else 0.3,
                                             top_k = 5,
                                             repetition_penalty=1.05)
    mysql_db_handler(full_output, json_data, generation_kwargs, question, input_data, task)


async def llm_default_handler(task: LLMTask, task_id, manager: ConnectionManager, websocket: WebSocket, input_data,
                              user_id: int):
    """默认对话模式， 直接使用大模型"""
    generation_kwargs = input_data["generation_params"]
    question = input_data["prompt"]
    recent_chat = []
    with SessionManager() as db:
        sessions = crud.get_chat_history_by_session_id(db, {"session_id": input_data["session_id"], "is_delete": False})
        chat_history = []
        my_dict = {}
        for row in sessions:
            my_dict["prompt"] = row.prompt
            my_dict["answer"] = row.answer
            chat_history.append(my_dict)
            my_dict = {}
    if len(chat_history) > 0:
        if len(chat_history) > 2:
            recent_chat = chat_history[-3:]
        else:
            recent_chat = chat_history
        if "glm" in LLM_MODEL:
            print("GLM")
            prompt4history = glm_format_chat_history_list(recent_chat)
            llm_input = prompt4history + "[Rround {}]\n\n问：{}\n\n答：".format(len(recent_chat), question)
        elif "chuan" in LLM_MODEL:
            print("Baichuan")
            llm_input = baichuan_format_chat_history_list(recent_chat) + '<reserved_106>' + question + '<reserved_107>'
        else:   
            print("其他模型")
            prompt4history = (('以下是你与用户的历史对话.\n') +
                            format_chat_history_list(recent_chat) +
                            ('(以上历史对话仅供参考)\n 请你用流畅的语言回答接下来的一个问题，需要注意你的回答中绝对不可以有对话形式出现，仅回答以下这个问题：') +
                            question + '\n请回答:')
            llm_input = instruction.format(prompt4history)
    else:
        if "chuan" in LLM_MODEL:
            llm_input = '<reserved_106>' + question + '<reserved_107>'
        else:
            llm_input = instruction.format(question)
    print(llm_input)
    full_output, extra_info = await llama_model.generate(task, llm_input, manager, websocket,
                                             max_length=generation_kwargs["max_length"] if generation_kwargs[
                                                 "max_length"] else 2048,
                                             do_sample=True,
                                             top_p=generation_kwargs["top_p"] if generation_kwargs[
                                                 "top_p"] else 0.85,
                                             temperature=generation_kwargs["temperature"] if generation_kwargs[
                                                 "temperature"] else 0.3,
                                             top_k = 5,
                                             repetition_penalty=1.05)
    print("gene finished" + full_output)
    mysql_db_handler(full_output, None, generation_kwargs, question, input_data, task)


thread_test_pool_executor = ThreadPoolExecutor(max_workers=5, thread_name_prefix="llm_generator_test_")


def wrap_llm_handler_thread(llm_handler_fn, task_id, manager: ConnectionManager, websocket: WebSocket, input_data,
                            user_id: int):
    task = task_queue.get_user_llm_task(user_id)
    future = thread_test_pool_executor.submit(wrap_coroutine_fn, llm_handler_fn, task, task_id, manager, websocket,
                                              input_data, user_id)
    task_queue.set_user_task_future(user_id, future)


async def llm_test_handler(task: LLMTask, task_id, manager: ConnectionManager, websocket: WebSocket, input_data,
                           user_id: int):
    try:
        for i in range(2):
            i = 30 - i
            print(f'当前 运行中的 task :{task}')
            if task.is_stopped:
                await manager.send_json(websocket_response_data(task_id, code=WSStatus.STOPPED.value,
                                                                msg=f"Stopping !! just a test, holding {i}s"),
                                        websocket)
                break
            await manager.send_json(
                websocket_response_data(task_id, code=WSStatus.RUNNING.value, msg=f"just a test, holding {i}s"),
                websocket)
            await asyncio.sleep(1)
        chat_history = {}
        chat_history["answer"] = 'full_output'
        chat_history["extra_info"] = [{"page": 27, "doc_id": "1575270108132107477995",
                                       "content": "混凝土拌合物的检验方法是检测项目均在拌和楼机口取样，按DL/T 5112与 DL/T 5433的要求检验。",
                                       "doc_name": "1575270108132107477999.json"},
                                      {"page": 12, "doc_id": "1575270108132107477994",
                                       "content": "干式电抗器及消弧线圈安装工程质量等级评定标准中的外观检查的检验方法是目测与手触摸检查、目测与绝缘电阻表检查、目测与扳手检查。",
                                       "doc_name": "1575270108132107477999.json"},
                                      {"page": 10, "doc_id": "1575270108132107477994",
                                       "content": "DL∕T5113.5-2012 水电水利基本建设工程 单元工程质量等级评定标准 第5部分：发电电气设备安装工程中的质量等级分为合格与优良。",
                                       "doc_name": "1575270108132107477999.json"}]
        chat_history["model_param"] = {"temperature": 0.9, "top_p": 0.7, "max_length": 2048}
        chat_history["created_time"] = datetime.datetime.now()
        chat_history["prompt"] = 'llm_input'
        chat_history["session_id"] = input_data["session_id"]
        chat_history['likes'] = False
        chat_history['dislikes'] = False
        chat_history['comment'] = None
        chat_history['dislike_tag'] = None
        with SessionManager() as db:
            if input_data.get("chat_history_id") is not None:
                crud.update_last_chat(db, chat_history)
            else:
                crud.create_dialogue(db, chat_history)
    except Exception as exc:
        print(str(exc))
        traceback.print_exc()
    else:
        pass


async def run_task():
    """
    Remove llm_task records in background Thread
    :return:
    """
    while True:
        try:
            for future in concurrent.futures.as_completed(task_queue.future_llm_task_map):
                llm_task: LLMTask = task_queue.future_llm_task_map[future]
                rsp = websocket_response_data(task_id=llm_task.task_id, code=WSStatus.FINISHED)
                rsp["session_id"] = llm_task.session_id
                rsp["chat_history_id"] = llm_task.chat_history_id
                rsp["extra_info"] = llm_task.extra_info
                if future.exception() is not None:
                    """ with exception """
                    print(f'llm_task_id:{llm_task.task_id} raise exception : {str(future.exception())} ')
                    rsp["code"] = WSStatus.TASK_ERROR.value
                    rsp["status"] = WSStatus.TASK_ERROR.phrase
                    rsp["msg"] = f"任务异常终止"

                await llm_task.manager.user_send_json(llm_task.user_id, rsp)
                print(f'llm_task_id:{llm_task.task_id}  is done')

                if llm_task.task_id == task_queue.get_user_task_id(llm_task.user_id):
                    """ task_id is the current record in user task_id_queue"""
                    task_queue.remove_user_task(llm_task.user_id)
                task_queue.remove_back_task(llm_task.task_id)

        except Exception as exc:
            print(f'background thread exception: {str(exc)}')
        else:
            pass
        await asyncio.sleep(10)


class BackTaskProcessThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        self.uname = 'BackTask'
        super().__init__(target=self.main, *args, **kwargs)

    def main(self):
        print(f'start back task thread')
        asyncio.run(run_task())


background_task_thread = BackTaskProcessThread()
background_task_thread.setDaemon(True)
background_task_thread.start()
