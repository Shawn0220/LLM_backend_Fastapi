"""
Created on 2022-05-26
@author:
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ENV = os.environ.get('ENV_PROFILE')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD')
MYSQL_DATABASE = os.environ.get('MYSQL_DB')
MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT'))


if ENV == 'dev':  # 开发模式
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://"
    connect_args = {
        "user": MYSQL_USER,
        "password": MYSQL_PASSWORD,
        "database": MYSQL_DATABASE,
        "host": MYSQL_HOST,
        "port": MYSQL_PORT,
    }
elif ENV == 'test':  # 测试模式
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://"
    connect_args = {
        "user": "root",
        "password": "root",
        "database": "fast_api_demo",
        "host": "127.0.0.1",
        "port": 3306,
    }
elif ENV == 'prod':  # 生产模式
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://"
    connect_args = {
        "user": MYSQL_USER,
        "password": MYSQL_PASSWORD,
        "database": MYSQL_DATABASE,
        "host": MYSQL_HOST,
        "port": MYSQL_PORT,
    }
else:  # 默认值
    # SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost/fast_api"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://"
    connect_args = {
        "user": "root",
        "password": "root",
        "database": "fast_api_demo",
        "host": "127.0.0.1",
        "port": 3306,
    }

engine = create_engine(SQLALCHEMY_DATABASE_URI, connect_args=connect_args, pool_pre_ping=True, pool_size=32, max_overflow=64)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base(engine)
