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
from typing import Optional
from pymilvus import (
    connections,
    utility,
    Collection,
)
from apps.chat.llm_handlers import model, instruction, tokenizer, transformer
router = APIRouter(
    prefix="/api/admin",
    tags=["admin模块"])

ENV = os.environ.get('ENV_PROFILE')

##### 管理员 提示词模板
@router.get('/prompt_tree', response_model=schemas.BaseOut, summary='树结构返回分类及模板')
async def template_tree(db: Session = Depends(get_db)):
    types = crud.select_all_prompt_template_type(db)
    temp_dict = {}
    prompt_type_list = []
    for row in types:
        print(row.p_type)
        temp_dict["p_id"] = row.p_id
        temp_dict["p_type"] = row.p_type
        temp_dict["cnt"] = row.cnt
        temp_dict["logo"] = row.logo
        prompt_type_list.append(temp_dict)
        temp_dict = {}
    templates = crud.select_all_prompt_template(db, True)

    templates_list = [{"id": row.id, "instruction": row.instruction, "notes": row.notes, "p_type": row.p_type, "is_available": row.is_available} for row in templates]
    
    for type in prompt_type_list:
        now_ptype = type["p_type"]
        type["children"] = []
        for template in templates_list:
            if template["p_type"]==now_ptype:
                type["children"].append(template)
    data = { "tree" : prompt_type_list }
    return util_response(data=data)

@router.get('/prompt_template_type', response_model=Page[schemas.PromptTemplateTypeOut], summary='管理员查询所有提示词模板分类')
async def template_type_list(db: Session = Depends(get_db)):
    types = crud.select_all_prompt_template_type(db)
    temp_dict = {}
    prompt_type_list = []
    for row in types:
        print(row.p_type)
        temp_dict["p_id"] = row.p_id
        temp_dict["p_type"] = row.p_type
        temp_dict["cnt"] = row.cnt
        temp_dict["logo"] = row.logo
        prompt_type_list.append(temp_dict)
        temp_dict = {}
    data = {
        "total" : len(prompt_type_list),
        "list" : prompt_type_list
    }
    return util_response(data=data)
    # data = {
    #     "total": paginate(sessions).total,
    #     "list": [i.dict() for i in paginate(sessions).items]
    # }
    # return util_response(data=data)


@router.get('/prompt_template', response_model=Page[schemas.PromptTemplateOut], summary='管理员根据分类查询提示词模板')
async def template_list(p_type_id: Optional[int]=None, db: Session = Depends(get_db)):
    templates = crud.select_all_prompt_template_by_type(db, p_type_id)
    template_lst =  [{"instruction": row.Prompt_template.instruction, "notes": row.Prompt_template.notes, "is_available":row.Prompt_template.is_available} for row in templates]
    data = {
        "total": len(template_lst),
        "list": template_lst
    }
    return util_response(data=data)


@router.post('/prompt_template_type', response_model=schemas.BaseOut, summary='管理员增加模板分类')
async def prompt_template_type_create(item: schemas.PromptTemplateTypeIn,
                                 db: Session = Depends(get_db)):
    item = item.dict()
    crud.add_prompt_template_type(db, item)
    return util_response()


@router.post('/prompt_template', response_model=schemas.BaseOut, summary='管理员增加模板')
async def prompt_template_create(item: schemas.PromptTemplateIn,
                                 db: Session = Depends(get_db)):
    item = item.dict()
    crud.add_prompt_template(db, item)
    return util_response()


@router.put('/prompt_template_type/{pk}', response_model=schemas.BaseOut, summary='管理员修改模板分类')
async def prompt_template_type_update(item: schemas.PromptTemplateTypeIn, pk: int,
                                 db: Session = Depends(get_db)):
    item = item.dict()
    crud.update_prompt_template_type(db, item, pk)
    return util_response()


@router.put('/prompt_template/{pk}', response_model=schemas.BaseOut, summary='管理员修改提示词模板')
async def prompt_template_update(item: schemas.PromptTemplateIn, pk: int,
                                 db: Session = Depends(get_db)):
    item = item.dict()
    crud.update_prompt_template(db, item, pk)
    return util_response()


@router.delete('/prompt_template_type/{pk}', response_model=schemas.BaseOut, summary='管理员删除提示词模板分类')
async def prompt_template_type_delete(pk: int, db: Session = Depends(get_db)):
    crud.delete_prompt_template_type(db, pk)
    return util_response()


@router.delete('/prompt_template/{pk}', response_model=schemas.BaseOut, summary='管理员删除提示词模板')
async def prompt_template_delete(pk: int, db: Session = Depends(get_db)):
    crud.delete_prompt_template(db, pk)
    return util_response()


@router.put('/prompt_template_available/{pk}', response_model=schemas.BaseOut, summary='管理员上线/下线提示词模板')
async def prompt_template_launch(pk: int, db: Session = Depends(get_db)):
    crud.launch_takedown_prompt_template(db, pk)
    return util_response()


@router.get('/feedback', response_model=Page[schemas.FeedbackOut], summary='查看反馈')
async def feedback_list(search_keyword: Optional[str]=None, feedback_type: Optional[str]=None, dislike_reason: Optional[str]=None, db: Session = Depends(get_db)):
    item = {"search_keyword" : search_keyword, "feedback_type" : feedback_type, "dislike_reason" : dislike_reason}
    item = {key: value for key, value in item.items() if value is not None}
    feedbacks = crud.get_chat_feedbacks(db, item)
    feedbacks_list = [{"id": row.ChatHistory.id, "session_id": row.ChatHistory.session_id, "prompt": row.ChatHistory.prompt, "answer": row.ChatHistory.answer, "like_flag": row.ChatHistory.like_flag,"dislike_tag": row.ChatHistory.dislike_tag, "comment": row.ChatHistory.comment, "comment_time": row.ChatHistory.comment_time, "user_id": row.Session.user_id} for row in feedbacks]
    data = {
        "total": len(feedbacks_list),
        "list": feedbacks_list
    }
    return util_response(data=data)

@router.delete('/feedback/{pk}', response_model=schemas.BaseOut, summary='管理员删除用户反馈')
async def del_feedback(pk: int, db: Session = Depends(get_db)):
    crud.del_user_feedback(db, pk)
    return util_response()