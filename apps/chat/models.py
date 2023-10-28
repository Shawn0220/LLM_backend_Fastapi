"""
@description:创建数据表
"""
import datetime
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, JSON
from sqlalchemy.orm import relationship
from databases import Base


# 对话
class Session(Base):
    __tablename__ = "chat_session"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True, doc='对话id')
    user_id = Column(Integer, nullable=False, index=True, doc='用户ID')
    name = Column(String(255), nullable=False, doc='对话名称')
    is_delete = Column(Boolean, nullable=True, default=False, doc='是否删除')
    created_time = Column(DateTime, default=datetime.datetime.now, doc='创建时间')
    updated_time = Column(DateTime, default=datetime.datetime.now, doc='更新时间')
    assistant_type = Column(Integer, default=0, doc='对话类型')


class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    # user_id = Column(Integer,  ForeignKey("user.id"), index=True, doc='用户ID')
    session_id = Column(Integer, ForeignKey("chat_session.id"), index=True, doc='对话ID')
    prompt = Column(String(2048), doc='prompt')
    answer = Column(String(2048), doc='answer')
    likes = Column(Boolean, default=False, doc='好评')
    dislikes = Column(Boolean, default=False, doc='差评')
    like_flag = Column(String(10), default='0', doc = '无/好评/差评')
    comment = Column(String(255), default='', nullable=True, doc='评价')
    # session = relationship("Session", back_populates="session_detail")  # 方便查询，不生成字段
    prompt_mode_id = Column(Integer, default=1, doc='提示词模式')
    created_time = Column(DateTime, default=datetime.datetime.now, doc='创建时间')
    # updated_time = Column(DateTime, default=datetime.datetime.now(), doc='更新时间')
    model_param = Column(JSON, doc="模型参数")
    dislike_tag = Column(JSON, default=[], doc='差评标签')
    extra_info = Column(JSON, doc='附加信息')
    is_delete = Column(Boolean, default=False,doc='删除')
    comment_time = Column(DateTime, doc='用户评价时间')
    # provision_id = Column(Integer, ForeignKey("provision.id"), doc='条文id')
    # Define the relationship with the Provision model
    # provision = relationship('Provision', backref='chat_history')

    # def __repr__(self):
    #     return f"ChatHistory(id={self.id}, provision_id={self.prompt}, session_id={self.provision_id})"


class UserPromptTemplates(Base):
    __tablename__ = "user_saved_prompt"

    # id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True, index=True)
    mode_id = Column(Integer, primary_key=True)
    custom = Column(String(255), default='', doc='用户自定义')


#
class Provision(Base):
    __tablename__ = "provision"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(2048), default='', nullable=True, doc='条文内容')
    doc_id = Column(String(255), doc='文件id')
    page = Column(Integer, doc='条文所在页码')
    doc_name = Column(String(255), default='', nullable=True, doc='文件名')
    key_word = Column(String(255))
    title = Column(String(255))

    def __repr__(self):
        return f"{self.id, self.content, self.doc_id, self.page, self.doc_name}"

class Prompt_template(Base):
    __tablename__  = "prompt_mode"

    id = Column(Integer, primary_key=True)
    instruction = Column(String(255))
    notes = Column(String(255))
    is_available = Column(Boolean)
    p_type = Column(String(255))


class PromptTemplateType(Base):
    __tablename__  = "prompt_type"

    p_id = Column(Integer, primary_key=True)
    p_type = Column(String(255))
    cnt = Column(Integer, default=0, doc='该类模板计数')
    logo = Column(String(255))