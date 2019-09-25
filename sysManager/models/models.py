from flask_login import UserMixin
from sqlalchemy import Integer, String, Column, UniqueConstraint, Index

from sysManager.config.database import pgsql, init_db


# TODO: 参考注释 --> https://www.jianshu.com/nb/32362137

class Users(UserMixin, pgsql.Base):
    __tablename__ = 'users'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50), unique=True)
    email = Column('email', String(120), unique=True)
    password = Column('password', String(120), unique=False)

    def __init__(self, id=None, name=None, email=None, password=None):
        self.id = id
        self.name = name
        self.email = email
        self.password = password

    __table_args__ = (
        # 设置联合唯一
        UniqueConstraint('name', 'password', name='users_name_pass'),
        # 建立索引
        Index('users_id_name', 'name'),
    )

    # 进行数据json转换
    def to_json(self):
        dict = self.__dict__
        if '_sa_instance_state' in dict:
            del dict['_sa_instance_state']
        return dict


class Units(pgsql.Base):
    __tablename__ = 'units'
    id = Column('id', Integer, primary_key=True)
    name = Column('name', String(50), unique=True)

    def __init__(self, id=None, name=None):
        self.id = id
        self.name = name

    __table_args__ = (
        # 设置联合唯一
        UniqueConstraint('id', 'name', name='units_id_name'),
        # 建立索引
        Index('units_name', 'name'),
    )

    # 进行数据json转换
    def to_json(self):
        dict = self.__dict__
        if '_sa_instance_state' in dict:
            del dict['_sa_instance_state']
        return dict


# TODO: 注意这个函数
init_db()
