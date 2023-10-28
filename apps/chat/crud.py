"""
@description:增删改查的数据库操作
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException, status
from apps.chat import models
from utils.custom_config import SECRET_KEY, ALGORITHM
from sqlalchemy import update, and_, not_
import datetime
from sqlalchemy.orm import joinedload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db: Session, username: str):
    """
    根据用户名查询用户
    :param db:
    :param username:
    :return:
    """
    return db.query(models.Session).filter(models.Session.username == username).first()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """
    创建token信息
    :param data:
    :param expires_delta:
    :return:
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def update_dialogue(db: Session, data: dict, pk: int):
    update_statement = (
        update(models.ChatHistory)
        .where(models.ChatHistory.id == pk)
        .values(**data)
    )
    db.execute(update_statement)
    db.commit()


def create_dialogue(db: Session, data: dict):
    db_chat_history = models.ChatHistory(**data)
    db.add(db_chat_history)
    db.commit()
    db.refresh(db_chat_history)
    return db_chat_history


def create_session(db: Session, data: dict, user_id: int):
    """
    创建对话
    :param db:
    :param data:
    :return:
    """
    if data['assistant_type'] == 'engineering':
        existing_session = db.query(models.Session).filter_by(user_id=data['user_id'], assistant_type='engineering', is_delete=False).first()
        if existing_session:
            print('User\'s [engineering assistant] already exists.')
            return {"session_id":existing_session.id, "assistant_type":existing_session.assistant_type, "name":existing_session.name, "created_time":existing_session.created_time}
    if data['assistant_type'] == 'hydro':
        existing_session = db.query(models.Session).filter_by(user_id=data['user_id'], assistant_type='hydro', is_delete=False).first()
        if existing_session:
            print('User\'s [hydro assistant] already exists.')
            return {"session_id":existing_session.id, "assistant_type":existing_session.assistant_type, "name":existing_session.name, "created_time":existing_session.created_time}
    db_session = models.Session(**data)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)

    return {"session_id":db_session.id, "assistant_type":db_session.assistant_type, "name":db_session.name, "created_time":db_session.created_time}


def delete_session(db: Session, pk: dict):
    update_statement = (
        update(models.Session)
        .where(models.Session.session_id == pk)
        .values(is_delete=True)
        .values(updated_time=datetime.datetime.now())
    )
    db.execute(update_statement)
    db.commit()


def get_user_prompt_templates_list(db: Session, pk: int):
    """
    用户保存的提问模板查询
    """
    sessions = db.query(models.UserPromptTemplates).filter_by(user_id=pk)

    return sessions


def get_user_session_list(db: Session, item: dict, flag: str):
    """
    用户列表查询
    """
    if flag:
        sessions = db.query(models.Session).order_by(models.Session.id.desc()).filter_by(**item, assistant_type="default")
    else:
        sessions = db.query(models.Session).order_by(models.Session.id.desc()).filter_by(**item).filter(models.Session.assistant_type != "default")
    return sessions



def select_all_prompt_template_type(db: Session):
    """
    查询所有模板分类
    """
    sessions = db.query(models.PromptTemplateType).filter_by()
    return sessions


def select_all_prompt_template(db: Session, is_show_all):
    """
    查询所有模板
    """
    if is_show_all:
        sessions = db.query(models.Prompt_template).filter_by()
    else:
        sessions = db.query(models.Prompt_template).filter_by(is_available=True)
    return sessions


def select_all_prompt_template_by_type(db: Session, p_type_id):
    query = db.query(models.Prompt_template, models.PromptTemplateType)
    query = query.join(models.PromptTemplateType, models.Prompt_template.p_type == models.PromptTemplateType.p_type)
    query = query.filter(models.PromptTemplateType.p_id==p_type_id)
    templates = query.all()
    return templates


def get_session_id(db: Session, pk: int):
    """
    根据id值查询用户
    """
    user = db.query(models.Session).filter_by(id=pk).first()
    return user


def update_last_chat(db: Session, item: dict):
    s_id = item["session_id"]
    chat_history = db.query(models.ChatHistory).filter_by(session_id=s_id).order_by(models.ChatHistory.id.desc()).first()
    update_statement = (
        update(models.ChatHistory)
        .where(models.ChatHistory.id == chat_history.id)
        .values(**item)
    )
    db.execute(update_statement)
    db.commit()
    return chat_history


def update_session_name(db: Session, pk: int, new_name: str):
    update_statement = (
        update(models.Session)
        .where(models.Session.id == pk)
        .values(**{'name': new_name})
    )
    db.execute(update_statement)
    db.commit()


def dialogue_feedback(db: Session, item:dict):
    chat_history_id = item["chat_history_id"]
    del item["chat_history_id"]
    item["comment_time"] = datetime.datetime.now()
    update_statement = (
        update(models.ChatHistory)
        .where(models.ChatHistory.id == chat_history_id)
        .values(**item)
    )
    db.execute(update_statement)
    db.commit()


def get_chat_history_by_session_id(db: Session, item: dict):
    # chat_history = db.query(models.ChatHistory).filter_by(session_id=pk)
    chat_history = db.query(models.ChatHistory).filter_by(**item)

    # 使用join()方法连接ChatHistory和Provision表
    # result = chat_history.join(models.Provision, models.ChatHistory.provision_id == models.Provision.id)

    return chat_history


def user_edit(db: Session, pk: int, item: dict):
    print(item)
    res = db.query(models.Session).filter_by(id=pk).update(
        item)  # {'username': '利斯在', 'email': None, 'is_active': True}
    print(f'res{res}')
    db.commit()


def session_delete(db: Session, pk: int):
    update_statement = (
        update(models.Session)
        .where(models.Session.id == pk)
        .values(is_delete=True)
        .values(updated_time=datetime.datetime.now())
    )
    db.execute(update_statement)
    db.commit()


def user_delete(db: Session, pk: int):
    """
    用户删除
    """
    db.query(models.Session).filter_by(id=pk).delete()
    db.commit()


def save_prompt_template(db: Session, data: dict):
    db_session = models.UserPromptTemplates(**data)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)


def delete_saved_mode(db: Session, u_id: int, m_id: int):
    db.query(models.UserPromptTemplates).filter_by(user_id=u_id, mode_id=m_id).delete()
    db.commit()


def get_provision_by_co_id(db: Session, co_id: int):
    provision = db.query(models.Provision).filter_by(id=co_id).first()
    return provision


def delete_chat_history(db: Session, item: dict):
    update_statement = (
        update(models.ChatHistory)
        .where(models.ChatHistory.id >= item["chat_history_id"], models.ChatHistory.session_id == item["session_id"])
        .values(is_delete=True)
    )
    db.execute(update_statement)
    db.commit()


def add_prompt_template_type(db: Session, item: dict):
    db_session = models.PromptTemplateType(**item)
    db.add(db_session)
    db.commit()
    db.refresh(db_session)


def add_prompt_template(db: Session, item: dict):
    db_session = models.Prompt_template(**item)
    db.add(db_session)

    # 增加模板后，向模板分类表计数器作相应修改
    prompt_type = db.query(models.PromptTemplateType).filter_by(p_type=item['p_type']).first()
    print(prompt_type)
    if prompt_type:
        cnt = prompt_type.cnt + 1
        update_statement = (
            update(models.PromptTemplateType)
            .where(models.PromptTemplateType.p_type==item['p_type'])
            .values(cnt=cnt)
        )
        db.execute(update_statement)

    db.commit()
    db.refresh(db_session)


def update_prompt_template_type(db: Session, item: dict, pk: int):
    temp_type = db.query(models.PromptTemplateType.p_type).filter_by(p_id=pk).scalar()
    update_template_statement = (
        update(models.Prompt_template)
        .where(models.Prompt_template.p_type == temp_type)
        .values(p_type=item["p_type"])
    )
    db.execute(update_template_statement)    
    update_statement = (
        update(models.PromptTemplateType)
        .where(models.PromptTemplateType.p_id == pk)
        .values(**item)
    )
    db.execute(update_statement)
    db.commit()


def update_prompt_template(db: Session, item: dict, pk: int):
    update_statement = (
        update(models.Prompt_template)
        .where(models.Prompt_template.id == pk)
        .values(**item)
    )
    db.execute(update_statement)
    db.commit()


def delete_prompt_template_type(db: Session, pk: int):
    db.query(models.PromptTemplateType).filter_by(p_id=pk).delete() 
    db.commit()


def delete_prompt_template(db: Session, pk: int):
    to_delete_template = db.query(models.Prompt_template).filter_by(id=pk).first()
    db.query(models.Prompt_template).filter_by(id=pk).delete()
    p_type = to_delete_template.p_type
    try:
        prompt_type = db.query(models.PromptTemplateType).filter_by(p_type=p_type).first()
        cnt = prompt_type.cnt - 1
        update_statement = (
            update(models.PromptTemplateType)
            .where(models.PromptTemplateType.p_type==p_type)
            .values(cnt=cnt)
        )
        db.execute(update_statement)
    except Exception as e:
        print("级联更新提示词分类表计数器失败")
        
    db.commit()


def get_chat_feedbacks(db: Session, item: dict):
    query = db.query(models.ChatHistory, models.Session)
    query = query.join(models.Session, models.ChatHistory.session_id == models.Session.id)
    query = query.filter(models.ChatHistory.like_flag!=0)
    has_search_keyword = False
    if "search_keyword" in item:
        query = query.filter( and_(models.ChatHistory.prompt.like('%'+item["search_keyword"]+'%')))
        has_search_keyword = True
    case_dict = {
        '0': 0,
        '1': 1,
        '2': 2
    }
    if "feedback_type" in item:
        if not has_search_keyword and case_dict[item["feedback_type"]]!=0:
            query = query.filter(models.ChatHistory.like_flag!=0)
        query = query.filter(models.ChatHistory.like_flag==case_dict[item["feedback_type"]])
    if "dislike_reason" in item:
        query = query.filter(models.ChatHistory.dislike_tag.contains(item["dislike_reason"]))
    feedbacks = query.all()
    return feedbacks
    

def launch_takedown_prompt_template(db: Session, pk: int):
    update_statement = (
        update(models.Prompt_template)
        .where(models.Prompt_template.id == pk)
        .values(is_available=not_(models.Prompt_template.is_available))
    )
    db.execute(update_statement)
    db.commit()


def del_user_feedback(db: Session, pk: int):
    item = {'like_flag':'0', 'dislike_tag':[], 'comment':None, 'comment_time':None}
    update_statement = (
        update(models.ChatHistory)
        .where(models.ChatHistory.id == pk)
        .values(**item)
    )
    db.execute(update_statement)
    db.commit()