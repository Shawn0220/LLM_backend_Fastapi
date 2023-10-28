"""
@description:用户模块依赖注入
"""
import warnings
from contextlib import contextmanager

from databases import SessionLocal


# 数据库依赖【需要数据库操作的路由用这个】
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@contextmanager
def SessionManager():
    db = SessionLocal()
    try:
        yield db
    except:
        # if we fail somehow rollback the connection
        warnings.warn("We somehow failed in a DB operation and auto-rollbacking...")
        db.rollback()
        raise
    finally:
        db.close()
