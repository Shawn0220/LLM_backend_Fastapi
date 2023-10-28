"""
@description:全局常用方法
"""
import uuid
import os
import datetime
from typing import Any, Callable
from utils.custom_config import MEDIA_ROOT

"""SQLAlchemy对象转换为字段格式"""
obj_to_dict: Callable[[Any], dict] = lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}


def get_file_path(instance, filename):
    """文件保存路径"""
    folder = instance.__class__.__name__.lower() + datetime.datetime.now().strftime("/%Y/%m/%d")
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(folder, filename)


def get_file_path_by_name(foldername, filename):
    """
    图片上传返回
    """
    folder = foldername.lower() + datetime.datetime.now().strftime("/%Y/%m/%d")
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return "%s/%s" % (folder, filename)


def format_chat_history_list(chathistory):
    result = ""
    current_length = 0
    for item in reversed(chathistory):
        prompt = item["prompt"]
        answer = item["answer"]
        formatted_item = f"用户提问:{prompt}\n你的回答:{answer}\n"

        if current_length + len(formatted_item) <= 1000:
            result = result + formatted_item 
            current_length += len(formatted_item)
        else:
            break
    return result


def glm_format_chat_history_list(chathistory):
    result = ""
    current_length = 0
    cnt = 1
    for item in reversed(chathistory):
        prompt = item["prompt"]
        answer = item["answer"]
        formatted_item = f"[Rround {cnt}]\n\n问：{prompt}\n\n答：{answer}\n\n"
        if current_length + len(formatted_item) <= 1000:
            result = result + formatted_item 
            current_length += len(formatted_item)
            cnt += 1
        else:
            break
    return result

def baichuan_format_chat_history_list(chathistory):
    result = ""
    current_length = 0
    cnt = 1
    for item in reversed(chathistory):
        prompt = item["prompt"]
        answer = item["answer"]
        formatted_item = f"<reserved_106>{prompt}<reserved_107>{answer}"
        if current_length + len(formatted_item) <= 1000:
            result = result + formatted_item 
            current_length += len(formatted_item)
            cnt += 1
        else:
            break
    print(result)
    return result


def file_path_delete(file_path):
    """
    根据文件路径删除
    """
    try:
        os.remove(os.getcwd() + str(file_path))
    except Exception as e:
        print(e)


def diff_delete_file(files, db_obj):
    """更新时判断、删除文件"""
    try:
        # 获取数据库内图片信息
        obj = db_obj.files.all()
        db_file = [i.file for i in obj]
        set_db_file = set(db_file)
        # 获取请求过来的图片信息
        set_files = ['/media' + i.split('/media')[-1] for i in files]
        set_files = set(set_files)
        diff_file = set_db_file.difference(set_files)
        for i in diff_file:
            file_path_delete(i)
    except Exception as e:
        print(e)


def save_file(file_name):
    """文件保存"""
    file = cache.get(file_name)
    if file:
        filename = os.path.join(MEDIA_ROOT, file_name)
        filename = filename.replace('\\', '/')
        pos = filename.rfind("/")
        filepath = filename[:pos]
        if not os.path.isdir(filepath):
            os.makedirs(filepath)
        with open(filename, 'wb') as f:
            for chunk in file.chunks():  # 分块写入文件
                f.write(chunk)
        cache.delete(file_name)

def get_suid():
    uid = str(uuid.uuid4())
    return ''.join(uid.split('-'))
