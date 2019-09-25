from sysManager.config.database import pgsql
from sysManager.models.models import Users, Units
import json


def inst_test():
    session = pgsql.db_session
    u1 = Users('1', 'zhangsan1', '111111111@qq.com', '1111111')
    u2 = Users('2', 'zhangsan2', '222222222@qq.com', '2222222')
    u3 = Users('3', 'zhangsan3', '333333333@qq.com', '3333333')
    u4 = Units('4', 'IBM公司')
    u5 = Units('5', '苹果公司')
    session.add(u1)
    session.add(u2)
    session.add(u3)
    session.add(u4)
    session.add(u5)
    session.commit()


def query_test():
    # session = pgsql.db_session
    # users = session.query(User)
    results = []
    users = Users.query.all()

    for user in users:
        results.append(user.to_json())

    units = Units.query.all()
    for unit in units:
        results.append(unit.to_json())
    return results
