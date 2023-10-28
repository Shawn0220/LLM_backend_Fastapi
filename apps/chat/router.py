"""
@author: HDEC
@description:用户模块路由
"""
from http import HTTPStatus
import os
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, HTTPException
from fastapi import Depends
from fastapi import Header
# from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from apps.chat.dependencies import SessionManager
from apps.chat import crud
from apps.chat import schemas
from apps.chat.dependencies import get_db
from apps.chat.llm_handlers import llm_generate_handlers, llm_stop_generate_handler, get_task_queue, stop_user_task
from apps.chat.websocket_manager import ConnectionManager
from utils.custom_pagination import Page
from utils.custom_response import util_response
from transformers import LlamaForCausalLM, LlamaTokenizer, TextIteratorStreamer
from pymilvus import (
    connections,
    utility,
    Collection,
)
from apps.chat.llm_handlers import model, instruction, tokenizer, transformer
router = APIRouter(
    prefix="/api/chat",
    tags=["chat模块"])

manager = ConnectionManager()

BERT_BASE_MODEL = os.environ.get('BERT_BASE_MODEL')

ENV = os.environ.get('ENV_PROFILE')

LLM_MODEL = os.environ.get('CHAT_MODEL')



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

@router.post('/test_llmQA', response_model=schemas.TestOut, summary='批量测试')
async def test_generate(item: schemas.TestIn, db: Session = Depends(get_db)):
    question = item.prompt
    max_length = item.max_length
    top_k = item.top_k
    top_p = item.top_p
    temperature = item.temperature
    repetition_penalty = item.repetition_penalty
    """知识库模式"""
    # generation_kwargs = {"max_length":max_length, "top_k":top_k, "top_p":top_p, "temperature":temperature}
    if item.do_sample:
        generation_kwargs = {"max_length":max_length, "top_k":top_k, "top_p":top_p, "temperature":temperature, "repetition_penalty":repetition_penalty, "do_sample":item.do_sample}
        baichuan_kwarges = {}
    else:
        generation_kwargs = {"max_length":max_length, "repetition_penalty":repetition_penalty}
        baichuan_kwarges = {}
        
    search_data = transformer.encode(question)
    res = collection.search(
        data=[search_data],  # Embeded search value
        anns_field="embedding",  # Search across embeddings
        param={"metric_type": "COSINE",},
        limit=item.milvus_topk,  # Limit to top_k results per search
        output_fields=['co_id'],  # Include title field in result
    )
    json_data = []
    this_json = {}
    knowledge_base = ''
    with SessionManager() as db:
        for hits_i, hits in enumerate(res):
            for hit in hits:
                co_id = hit.entity.get('co_id')
                fetch_provision_detail = crud.get_provision_by_co_id(db, co_id)
                this_json['doc_id'] = str(fetch_provision_detail.doc_id)
                this_json['content'] = str(fetch_provision_detail.content)
                this_json['page'] = int(fetch_provision_detail.page)
                this_json['doc_name'] = str(fetch_provision_detail.doc_name)
                this_json['key_word'] = str(fetch_provision_detail.key_word)
                this_json['title'] = str(fetch_provision_detail.title)
                knowledge_base += str(fetch_provision_detail.content)
                json_data.append(this_json)
                this_json = {}
    print(json_data)
    # llm_input = instruction.format("使用下列条文回答最后的问题，如果问题不能在条文中找到答案，请回复“对不起，我无法找到相关的规定”\n" + knowledge_base + "\n问题:" +question + "\n答:")
    llm_input= instruction.format("请参考下列条文之一回答最后的问题，如果问题不能在条文中找到答案，请回复“对不起，我无法找到相关的规定”:\n\n" 
                                   + knowledge_base + "\n## 问题:" +question + "\n\n## 答:\n")
    if "chuan" in LLM_MODEL:
            llm_input = '<reserved_106>' + llm_input + '<reserved_107>'
            llm_kwarges = baichuan_kwarges
    else:
        llm_kwarges = generation_kwargs
        
    inputs = tokenizer.encode(llm_input, return_tensors='pt').cuda()
    streamer = TextIteratorStreamer(tokenizer, skip_prompt=True, skip_special_tokens=True, timeout=300)
   
    generate_ids = model.generate(inputs, streamer=streamer, **llm_kwarges)
    llm_result = tokenizer.decode(generate_ids[:, len(tokenizer.encode(llm_input)) :][0])
    data = {
        "llm_response": llm_result,
        "citation": json_data
    }
    return util_response(data=data)

@router.post('/chat_history', response_model=schemas.BaseOut, summary='创建对话单条问答')
async def generate(item: schemas.DialogueIn, db: Session = Depends(get_db)):
    item = item.dict()
    del item['assistant_type']
    chat_history = crud.create_dialogue(db, item)
    return util_response(data=chat_history)


@router.post('/chat_history/{pk}', response_model=schemas.BaseOut, summary='修改对话单条问答')
async def generate(item: schemas.DialogueIn, pk: int,
                   db: Session = Depends(get_db)):
    item = item.dict()
    crud.update_dialogue(db, item, pk)
    return util_response()


@router.post('/chat_history_feedback', response_model=schemas.BaseOut, summary='用户反馈')
async def dialogue_likes(item: schemas.ChatFeedbackIn, db: Session = Depends(get_db)):
    item = item.dict()
    crud.dialogue_feedback(db, item)
    return util_response()


""" Session接口 """


@router.get('/session/{pk}', response_model=Page[schemas.SessionDialogueInfo], summary='对话详情')
async def session_list(pk: int, db: Session = Depends(get_db)):  # , Session_id: int = Header(None)):
    sessions = crud.get_chat_history_by_session_id(db, {"session_id": pk, "is_delete": False})
    chat_history = []
    my_dict = {}
    for row in sessions:
        my_dict["chat_history_id"] = row.id
        my_dict["prompt"] = row.prompt
        my_dict["answer"] = row.answer
        # my_dict["likes"] = row.likes
        # my_dict["dislikes"] = row.dislikes
        my_dict["like_flag"] = row.like_flag
        my_dict["comment"] = row.comment
        my_dict["created_time"] = row.created_time
        my_dict["dislike_tag"] = row.dislike_tag
        my_dict["extra_info"] = row.extra_info  # .dict()
        chat_history.append(my_dict)
        my_dict = {}
    # print(chat_history)
    data = {
        "total": paginate(sessions).total,
        "list": chat_history
    }
    return util_response(data=data)


@router.get('/session', response_model=Page[schemas.UserSessionInfo], summary='对话列表')
async def session_list(isDefault: bool = True,db: Session = Depends(get_db), x_current_user_id: int = Header(None)):
    user_id = x_current_user_id
    sessions = crud.get_user_session_list(db, {"user_id": user_id, "is_delete": False}, isDefault)
    chat_history_list = [i.dict() for i in paginate(sessions).items]
    for item in chat_history_list:
        if "id" in item:
            item["session_id"] = item.pop("id")
        if item["assistant_type"]=="engineering":
            item["icon"]='llmgongchengwenda'
            item['title']='工程知识问答'
            item['content']='请输入水电专业知识问题，我来生成答案'
        elif item["assistant_type"]=="hydro":
            item["icon"]='llmbaogaoshengcheng'
            item['title']='抽蓄可研报告生成'
            item['content']='告诉我抽蓄项目的信息，我来生成帮助生成科研报告的章节'
    data = {
        "total": paginate(sessions).total,
        "list":  chat_history_list
    }
    return util_response(data=data)


@router.post('/session', response_model=schemas.BaseOut, summary='创建对话')
async def session_create(item: schemas.SessionIn,
                         db: Session = Depends(get_db), x_current_user_id: int = Header(None)):
    item = item.dict()
    item["user_id"] = x_current_user_id
    data = crud.create_session(db, item, x_current_user_id)
    response_data = data
    return util_response(data=response_data)


@router.delete('/session/{pk}', response_model=schemas.BaseOut, summary='删除对话')
async def session_delete(pk: int, db: Session = Depends(get_db)):  # item: schemas.DeleteIn
    crud.session_delete(db, pk)
    return util_response()


@router.put('/session/{pk}', response_model=schemas.BaseOut, summary='修改对话名称')
async def session_delete(pk: int, item: schemas.UpdateSessionNameIn, db: Session = Depends(get_db)):
    crud.update_session_name(db, pk, item.name)
    return util_response()


@router.get('/prompt_template', response_model=Page[schemas.PromptTemplateOut], summary='用户查询所有提示词模板')
async def session_list(db: Session = Depends(get_db)):
    sessions = crud.select_all_prompt_template(db, False)
    data = {
        "total": paginate(sessions).total,
        "list": [i.dict() for i in paginate(sessions).items]
    }
    return util_response(data=data)


###### 用户 提示词模板

@router.post('/prompt_template/favorate/{pk}', response_model=schemas.BaseOut, summary='用户收藏模板')
async def session_create(item: schemas.SaveTemplateIn, pk: int,
                         db: Session = Depends(get_db), x_current_user_id: int = Header(None)):
    # todo 从 request中 header 中获取userID
    user_id = x_current_user_id
    item = item.dict()
    item["user_id"] = user_id
    item["mode_id"] = pk
    # crud.save_prompt_template(db, item.user_id, item.prompt_id, item.custom)
    crud.save_prompt_template(db, item)
    return util_response()


@router.delete('/prompt_template/favorate/{pk}', response_model=schemas.BaseOut, summary='用户删除收藏模板')
async def session_delete(pk: int, db: Session = Depends(get_db), x_current_user_id: int = Header(None)):
    crud.delete_saved_mode(db, x_current_user_id, pk)
    return util_response()


@router.get('/prompt_template/favorate', response_model=Page[schemas.PromptTemplateInfo], summary='用户模板收藏列表')
async def session_list(db: Session = Depends(get_db), x_current_user_id: int = Header(None)):
    user_id = x_current_user_id
    sessions = crud.get_user_prompt_templates_list(db, user_id)
    data = {
        "total": paginate(sessions).total,
        "list": [i.dict() for i in paginate(sessions).items]
    }
    return util_response(data=data)


@router.delete('/chat_history', response_model=schemas.BaseOut, summary='删除问答历史')
async def session_delete(item: schemas.DelChatHistoryIdIn, db: Session = Depends(get_db)):
    item = item.dict()
    crud.delete_chat_history(db, item)
    return util_response()


@router.get('/chat_history/task', response_model=schemas.BaseOut, summary='对话任务')
async def session_delete(db: Session = Depends(get_db)):
    return util_response(data=get_task_queue())


@router.delete('/chat_history/task/{user_id}', response_model=schemas.BaseOut, summary='删除对话任务')
async def session_delete(user_id, item: schemas.ChatHistoryTaskIn, x_current_user_id: int = Header(None),
                         db: Session = Depends(get_db)):
    if stop_user_task(user_id) == -1:
        raise HTTPException(HTTPStatus.NOT_FOUND)
    return util_response(data=get_task_queue())


async def websocket_llm_handler(websocket: WebSocket, x_current_user_id: int):
    await manager.connect(user=x_current_user_id, websocket=websocket)
    try:
        while True:
            input_data = await websocket.receive_json()
            print(input_data)
            """判断是否生成 还是终止，处理模式等"""
            if input_data["action"] == "generate":
                # 创建一个生成Task，执行生成任务
                await llm_generate_handlers(manager, websocket, input_data, x_current_user_id)
            if input_data["action"] == "stop":
                # 接收一个任务id，关闭任务
                await llm_stop_generate_handler(manager, websocket, input_data, x_current_user_id)
    except WebSocketDisconnect:
        try:
            stop_user_task(x_current_user_id)
        except Exception as e:
            print('用户刷新断开连接')
        pass
    finally:
        # 关闭当前websocket 对应未完成的任务
        await manager.disconnect(user=x_current_user_id, websocket=websocket)