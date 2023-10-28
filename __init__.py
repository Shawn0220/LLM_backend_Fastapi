"""
常用命令
启动：uvicorn main:app --workers=4 --host=0.0.0.0 --port=8002 --reload

数据库相关：
创建一个alembic 文件/仓库：alembic init alembic
生成迁移文件：alembic revision --autogenerate -m "first add commit"
更新数据库到最新版本：alembic upgrade head

"""
