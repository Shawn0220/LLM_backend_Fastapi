"""
@author: HDEC
@description:用户模块路由
"""
import json
from datetime import timedelta
from fastapi import Depends, status, HTTPException
from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Form
# from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session
from apps.chat import schemas
from apps.chat import crud
from apps.chat.dependencies import get_db
from utils.custom_config import ACCESS_TOKEN_EXPIRE_MINUTES
from utils.custom_response import util_response
from utils.custom_pagination import Page
from utils.util import obj_to_dict
from fastapi import Header
from apps.chat import models
# from sentence_transformers import SentenceTransformer
# import llama_loader

# from apps.chat.llama_loader import llamaModel
from pymilvus import (
    connections,
    utility,
    FieldSchema, CollectionSchema, DataType,
    Collection,
)

import pymysql


def get_provision_by_co_id(co_id):
    # 连接数据库
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        password='12345678',
        database='llm_chat'
    )
    try:
        # 创建游标对象
        cursor = conn.cursor()
        # 执行查询语句
        sql = "SELECT * FROM provision WHERE id = %s"
        cursor.execute(sql, (co_id,))
        cursor.close()
        # 获取查询结果
        result = cursor.fetchone()
        return result
    finally:
        # 关闭连接
        conn.close()



'''
COLLECTION_NAME = 'standard_specification'  # Collection name
# DIMENSION = 768  # Embeddings size
# COUNT = 1000  # Number of vectors to insert
MILVUS_HOST = '172.20.64.60'
MILVUS_PORT = '19530'

""" 连接 Milvus """
connections.connect("default", host=MILVUS_HOST, port=MILVUS_PORT)
has = utility.has_collection(COLLECTION_NAME)
collection = Collection(name=COLLECTION_NAME)
collection.load()'''


router = APIRouter(
    prefix="/api/chat",
    tags=["chat模块"])


# transformer = SentenceTransformer('../qdrant_demo/bert_base_chinese')
# llama_model = llama_loader.llamaModel()
# model = llama_model.model
# streamer = llama_model.streamer
# instruction = llama_model.instruction
# tokenizer = llama_model.tokenizer

@router.post('/generate', response_model=schemas.BaseOut, summary='创建对话单条问答')
async def generate(item: schemas.DialogueIn,
                   db: Session = Depends(get_db)):
    # todo llm_model choose assistant type
    # model_type_or_knowledge = model_store.model(type)
    # todo model.set_param
    # param = item.model_param

    # todo 得到 prompt =》 embedding，赋值给下面这个
    # search_data = transformer.encode(item.prompt)
    search_data = [[1]*768]

    '''res = collection.search(
        data=search_data,  # Embeded search value
        anns_field="embedding",  # Search across embeddings
        param={},
        limit=3,  # Limit to top_k results per search
        output_fields=['co_id'],   # Include title field in result
    )

    json_data = []
    this_json = {}
    #
    knowledge_base = ''
    for hits_i, hits in enumerate(res):
        for hit in hits:
            co_id = hit.entity.get('co_id')
            fetch_provision_detail = get_provision_by_co_id(co_id)
            this_json['doc_id'] = fetch_provision_detail[3]
            this_json['content'] = fetch_provision_detail[1]
            this_json['page'] = fetch_provision_detail[4]
            this_json['doc_name'] = fetch_provision_detail[2]
            json_data.append(this_json)
            this_json = {}
            knowledge_base += fetch_provision_detail[1]'''

    '''
    # todo llm_input = llama_model.instruction.format(knowledge_base + item.prompt)
    llm_input = instruction.format(knowledge_base + item.prompt)

    # todo model.generate
    # todo input_ids = llama_model.tokenizer.encode(llm_input, return_tensors='pt').cuda()
    input_ids = tokenizer.encode(llm_input, return_tensors='pt').cuda()
    # todo generate_ids = llama_model.model.generate(input_ids, max_new_tokens=4096, streamer=llama_model.streamer)
    generate_ids = model.generate(input_ids, max_new_tokens=4096, streamer=streamer)
    # todo answer = llama_model.tokenizer.decode(generate_ids[:, len(llama_model.tokenizer.encode(prompt)):][0])
    answer = tokenizer.decode(generate_ids[:, len(llama_model.tokenizer.encode(llm_input)):][0])

    '''
    answer = '回答 temp_由todo生成'
    item.answer = answer
    # item.model_param =
    # todo create new chat_history record
    item = item.dict()
    # todo add key-value
    json_data = {}
    item['extra_info'] = json_data

    # del item['model_param']
    del item['assistant_type']
    crud.create_dialogue(db, item)
    # todo return output
    return util_response()


@router.post('/session', response_model=schemas.BaseOut, summary='创建对话')
async def session_create(item: schemas.SessionIn,
                         db: Session = Depends(get_db), x_current_user_id: int = Header(None)):
    # todo 从 request中 header 中获取userID
    user_id = x_current_user_id
    # item.user_id = user_id
    item = item.dict()
    item["user_id"] = user_id
    crud.create_session(db, item)
    return util_response()


@router.post('/prompt_save', response_model=schemas.BaseOut, summary='收藏模板')
async def session_create(item: schemas.SaveTemplateIn,
                         db: Session = Depends(get_db), x_current_user_id: int = Header(None)):
    # todo 从 request中 header 中获取userID
    user_id = x_current_user_id
    item = item.dict()
    item["user_id"] = user_id
    # crud.save_prompt_template(db, item.user_id, item.prompt_id, item.custom)
    crud.save_prompt_template(db, item)
    return util_response()


@router.post('/chat_history/update/{pk}', response_model=schemas.BaseOut, summary='用户反馈')
async def dialogue_likes(item: schemas.ChatFeedbackIn, db: Session = Depends(get_db)):
    crud.dialogue_feedback(db, item.chat_history_id, item.mode_controll, item.verify_or_cancel, item.comment)
    return util_response()


@router.delete('/session/{pk}', response_model=schemas.BaseOut, summary='删除对话')
async def session_delete(item: schemas.DeleteIn, db: Session = Depends(get_db)):
    crud.session_delete(db, item.session_id)
    return util_response()


@router.get('/session', response_model=Page[schemas.UserSessionInfo], summary='对话列表')
async def session_list(db: Session = Depends(get_db), x_current_user_id: int = Header(None)):
    user_id = x_current_user_id
    sessions = crud.get_user_session_list(db, {"user_id": user_id, "is_delete": False})
    data = {
        "total": paginate(sessions).total,
        "list": [i.dict() for i in paginate(sessions).items]
    }
    return util_response(data=data)


@router.get('/session/{pk}', response_model=Page[schemas.SessionDialogueInfo], summary='对话详情')
async def session_list(db: Session = Depends(get_db), Session_id: int = Header(None)):
    sessions = crud.get_chat_history_by_session_id(db, Session_id)
    chat_history = []
    my_dict = {}
    for row in sessions:
        my_dict["prompt"] = row.prompt
        my_dict["answer"] = row.answer
        my_dict["likes"] = row.likes
        my_dict["dislikes"] = row.dislikes
        my_dict["comment"] = row.comment
        my_dict["created_time"] = row.created_time
        # my_dict["provision_id"] = row.provision_id
        # 拼接上的provision变为成员
        my_dict["extra_info"] = row.extra_info  # .dict()
        # my_dict["content"] = row.provision.content
        # my_dict["page"] = row.provision.page
        # my_dict["doc_name"] = row.provision.doc_name
        chat_history.append(my_dict)
        my_dict = {}
    # print(chat_history)
    data = {
        "total": paginate(sessions).total,
        # "list": [i.dict() for i in paginate(sessions).items]
        "list": chat_history
    }
    return util_response(data=data)


@router.delete('/prompt_save', response_model=schemas.BaseOut, summary='删除模板')
async def session_delete(item: schemas.SaveTemplateIn, db: Session = Depends(get_db)):
    crud.delete_saved_mode(db, item.user_id, item.mode_id)
    return util_response()
