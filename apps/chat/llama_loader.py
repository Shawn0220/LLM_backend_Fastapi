import asyncio
import os
from threading import Thread
from typing import Dict
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import torch
from transformers import LlamaForCausalLM, LlamaTokenizer, TextIteratorStreamer
from transformers import AutoTokenizer, AutoModelForCausalLM
from sentence_transformers import SentenceTransformer

from apps.chat.llm_task import LLMTask
from apps.chat.schemas import websocket_response_data
from apps.chat.websocket_manager import ConnectionManager
from apps.chat.ws_status import WSStatus

CHAT_MODEL = os.environ.get('CHAT_MODEL')
BERT_BASE_MODEL = os.environ.get('BERT_BASE_MODEL')
transformer = SentenceTransformer(BERT_BASE_MODEL)

class LlamaModel:
    def __init__(self):
        self.instruction = """{} """
 
        # self.instruction = """[INST] <<SYS>>\nYou are a helpful, respectful and honest assistant. Always answer as helpfully as possible.\n<</SYS>>\n\n{} [/INST]"""
        self.model = AutoModelForCausalLM.from_pretrained(CHAT_MODEL, load_in_8bit=False, device_map='auto',
                                                      torch_dtype=torch.float16, trust_remote_code=True)
        self.model.eval()
        self.tokenizer = AutoTokenizer.from_pretrained(CHAT_MODEL, trust_remote_code=True)

    def __str__(self):
        return f"llamaModel(instruction='{self.instruction}')"

    async def generate(self, task: LLMTask, inputs, manager: ConnectionManager, websocket, extra_info=None, **kwargs):
        try:
            inputs = self.tokenizer.encode(inputs, return_tensors='pt').cuda()
            streamer = TextIteratorStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True, timeout=300)
            generation_kwargs = dict(input_ids=inputs, streamer=streamer, **kwargs)
            thread = Thread(target=self.model.generate, kwargs=generation_kwargs)
            thread.start()
            data = websocket_response_data(task_id=task.task_id,
                                          code=WSStatus.RUNNING.value,
                                          answer="",
                                          extra_info=extra_info)
            data["session_id"] = task.session_id
            data["chat_history_id"] = task.chat_history_id
            for new_text in streamer:
                if task.is_stopped:
                    return data["answer"]
                data["answer"] += new_text
                await manager.send_json(data, websocket)
            # print("================================================\n"+data["extra_info"][0]+"\n")
            # 遍历比较 answer 和 三个参考文献 的相似度
            # print(type(data["extra_info"]))
            # print("*LLM answer:*" + data["answer"])
            task.extra_info = extra_info
            answer_encode1024 = transformer.encode(data["answer"])
            try:
                sorted_extra_info_by_COS_answer = sorted(data["extra_info"], 
                                                        key=lambda x: 
                                                        cosine_similarity(
                                                            np.array([transformer.encode(x["content"])]).reshape(1,-1), 
                                                            np.array(answer_encode1024).reshape(1,-1)), 
                                                        reverse=True)
            # print(sorted_extra_info_by_COS_answer)
                data["extra_info"] = sorted_extra_info_by_COS_answer
                extra_info = sorted_extra_info_by_COS_answer
                task.extra_info = sorted_extra_info_by_COS_answer
            except Exception as e:
                print(str(e))
            await manager.send_json(data, websocket)
            return data["answer"], extra_info
        except Exception as e:
            print(f'llama_loader generate error: {str(e)}')
            raise e
        finally:
            thread.join(30)
