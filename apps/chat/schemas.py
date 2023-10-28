"""
@description:入参、出参的各个字段的类型进行定义
按照顺序写【基类，出参，入参】
"""
from typing import Optional
from pydantic import BaseModel, Field


# 响应基类
from apps.chat.ws_status import WSStatus


class BaseOut(BaseModel):
    err: int = Field(0, title='响应码')
    msg: str = Field('ok', title='响应码说明')
    data: dict = Field({}, title='响应内容')


class TestIn(BaseModel):
    prompt: str = Field(None, title='用户提问')
    max_length: int = Field(None, title='生成最大长度')
    top_k: int = Field(None, title='top K')
    top_p: float = Field(None, title='概率累计阈值')
    temperature: float = Field(None, title='温度')
    milvus_topk: int = Field(None, title='返回几条知识')
    repetition_penalty:float = Field(None, title='重复惩罚')
    do_sample:bool = Field(None, title='采样true then top_k is useful')


class TestOut(BaseModel):
    answer: str = Field(None, title='回答')
    extra_info: dict = Field(None, title='参考信息')


# 用户对话信息
class UserSessionInfo(BaseModel):
    id: int = Field(None, title='对话ID')
    name: str = Field(None, title='对话名称')
    assistant_type: str = Field(None, title='对话类型')

    class Config:
        orm_mode = True


# 用户模板信息
class PromptTemplateInfo(BaseModel):
    custom: str = Field(None, title='模板内容')
    mode_id: int = Field(None, title='模板id')

    class Config:
        orm_mode = True


class IsDefaultMode(BaseModel):
    IsDefault: bool = Field(None, title='是否普通模式')


class PromptTemplateTypeOut(BaseModel):
    p_id: int = Field(..., title='模板分类id')
    p_type: str = Field(..., title='模板分类名称')
    cnt: int = Field(..., title='已有该类模板数量')
    logo: str = Field(..., title='图标')


class PromptTemplateTypeIn(BaseModel):
    p_type: str = Field(..., title='模板分类名称')
    # cnt: int = Field(..., title='已有该类模板数量')
    logo: str = Field(..., title='图标')


# 默认模板信息
class PromptTemplateIn(BaseModel):
    instruction: str = Field(..., title='提示词模板内容')
    notes: str = Field(..., title='提示词模板备注')
    is_available: bool = Field(..., title='用户是否可见')
    p_type: str = Field(..., title='提示词分类')


class PromptTemplateOut(BaseModel):
    id: int = Field(..., title='提示词模板id')
    instruction: str = Field(..., title='提示词模板内容')
    notes: str = Field(..., title='提示词模板备注')
    p_type: str = Field(..., title='模板类型')
    is_available: bool = Field(..., title='是否对用户可见')
    class Config:
        orm_mode = True


class ChatFeedbackIn(BaseModel):
    chat_history_id: int = Field(..., title='问答id')
    # verify_or_cancel: bool = Field(..., title='确认或取消')
    like_flag: str =  Field(..., title='0取消点赞点踩/1点赞/2点踩')
    comment: str = Field(..., title='评论内容')
    dislike_tag: list = Field(..., title='差评标签')


class DialogueIn(BaseModel):
    session_id: int = Field(..., title='会话id')
    prompt: str = Field(..., title='用户提问')
    answer: str = Field(..., title='llm回答')
    assistant_type: str = Field(..., title='对话类型')
    model_param: dict = Field(..., title='模型参数')
    extra_info: dict = Field(..., title='参考信息')
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "session_id": 2,
    #             "prompt": 'test',
    #             "answer": 'asss1',
    #             "assistant_type": 0,
    #             "model_param": '123{123}'
    #         }
    #     }


class DeleteIn(BaseModel):
    session_id: int = Field(..., title='会话id')


class UpdateSessionNameIn(BaseModel):
    # session_id: int = Field(..., title='会话id')
    name: str = Field(..., title='新对话名称')


# 创建对话入参
class SessionIn(BaseModel):
    name: str = Field(..., title='对话名称')
    assistant_type: str = Field(..., title='对话类型')
    class Config:
        schema_extra = {
            "example": {
                "name": '666session_c123reate_test',
                "assistant_type": 'default',
            }
        }


class SaveTemplateIn(BaseModel):
    # mode_id: int = Field(..., title='提示词模板id')
    custom: str = Field(..., title='用户自定义')


# 用户对话信息
class SessionDialogueInfo(BaseModel):
    id: int = Field(None, title='问答编号')
    prompt: str = Field(None, title='提问')
    answer: str = Field(None, title='回答')
    likes: bool = Field(None, title='好评')
    dislikes: bool = Field(None, title='差评')
    comment: str = Field(None, title='评价')
    created_time: str = Field(None, title='创建时间')

    # provision_id: int = Field(None, title='条文id')
    # doc_id: int = Field(None, title='文件id')
    # content: str = Field(None, title='条文内容')
    # page: int = Field(None, title='条文页码')
    # doc_name: str = Field(None, title='文件名称')
    # extra_info:
    dislike_tag: list = Field(None, title='差评标签')
    extra_info: list = Field(None, title='附加信息')

    class Config:
        orm_mode = True

class DelChatHistoryIdIn(BaseModel):
    chat_history_id: int = Field(None, title='问答记录id')
    session_id: int = Field(None, title='会话id')


class ChatHistoryTaskIn(BaseModel):
    task_id: str = Field(None, title='任务ID')
    mode: str = Field(None, title='模式')
    action: str = Field(None, title='生成启动、停止')


class SelectFeedbackIn(BaseModel):
    search_keyword: Optional[str] = Field(None, title='问题关键词')
    feedback_type: Optional[str] = Field(None, title='反馈类型')
    dislike_reason: Optional[str] = Field(None, title='反馈原因')


class FeedbackOut(BaseModel):
    id: int = Field(None, title='反馈id(对话历史id)')
    session_id : int = Field(None, title='会话id')
    prompt: str = Field(None, title='问题')
    answer: str = Field(None, title='回答')
    like_flag: str = Field(None, title='反馈类型：无/好评/差评')
    dislike_tag: str = Field(None, title='反馈原因(差评原因)')
    comment: str = Field(None, title='自定义评价')
    comment_time: str = Field(None, title='评价时间')
    user_id: str = Field(None, title='用户id')

def websocket_response_data(task_id=None,
                            status=None,
                            code=None,
                            answer=None,
                            session_id=None,
                            chat_history_id=None,
                            msg=None,
                            extra_info=None):
    if code is not None:
        status = WSStatus(code).phrase
        if msg is None:
            msg = WSStatus(code).description

    """ websocket response data """
    return dict(task_id=task_id,
                status=status,
                code=code,
                answer=answer,
                session_id=session_id,
                chat_history_id=chat_history_id,
                msg=msg,
                extra_info=extra_info)