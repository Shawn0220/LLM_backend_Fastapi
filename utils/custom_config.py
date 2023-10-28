"""
@description:项目常量配置
"""
import os
from pathlib import Path

"""用户验证相关"""
SECRET_KEY = "764baa8d9ea4dc1c45a0ea99b0e7e75e15c261d807fca35bee511c0fd7e9b587"  # 密钥
ALGORITHM = "HS256"  # 加密方式
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 365  # 令牌过期时间【分钟】

"""项目根目录"""
BASE_DIR = Path(__file__).resolve().parent.parent

"""文件上传路径"""
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/upload')