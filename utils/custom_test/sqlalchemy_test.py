from sqlalchemy.dialects import mysql
from sqlalchemy import *
from sqlalchemy.orm import declarative_base, relationship, aliased, scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine("mysql+pymysql://root:root@127.0.0.1:3306/test?charset=utf8", echo=True, future=True)
Base = declarative_base(engine)
Session = sessionmaker(bind=engine)
session = scoped_session(Session)  # 基于scoped_session实现线程安全

"""一对多关系"""


class Users(Base):
    __tablename__ = 'users'  # 数据库表名称
    id = Column(Integer, primary_key=True)  # id 主键
    name = Column(String(32), index=True, nullable=False)  # name列，索引，不可为空
    age = Column(Integer, default=18)
    # email = Column(String(32), unique=True)
    # datetime.datetime.now不能加括号，加了括号，以后永远是当前时间
    # ctime = Column(DateTime, default=datetime.datetime.now)
    # extra = Column(Text, nullable=True)

    __table_args__ = (
        # UniqueConstraint('id', 'name', name='uix_id_name'), #联合唯一
        # Index('ix_id_name', 'name', 'email'), #索引
    )


class Hobby(Base):
    __tablename__ = 'hobby'
    id = Column(Integer, primary_key=True)
    caption = Column(String(50), default='篮球')


class Person(Base):
    __tablename__ = 'person'
    nid = Column(Integer, primary_key=True)
    name = Column(String(32), index=True, nullable=True)
    # hobby指的是tablename而不是类名
    hobby_id = Column(Integer, ForeignKey("hobby.id"))

    # 跟数据库无关，不会新增字段，只用于快速链表操作
    # 类名，backref用于反向查询
    hobby = relationship('Hobby', backref='pers')


"""多对多关系"""


class Boy2Girl(Base):
    __tablename__ = 'boy2girl'
    id = Column(Integer, primary_key=True, autoincrement=True)
    girl_id = Column(Integer, ForeignKey('girl.id'))
    boy_id = Column(Integer, ForeignKey('boy.id'))


class Girl(Base):
    __tablename__ = 'girl'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True, nullable=False)


class Boy(Base):
    __tablename__ = 'boy'

    id = Column(Integer, primary_key=True, autoincrement=True)
    hostname = Column(String(64), unique=True, nullable=False)

    # 与生成表结构无关，仅用于查询方便,放在哪个单表中都可以
    servers = relationship('Girl', secondary='boy2girl', backref='boys')


Base.metadata.create_all(engine)

session.close()
engine.dispose()
