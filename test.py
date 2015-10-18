#coding:utf-8
from simple_orm_mysql import *

db_config = {
    'host':"127.0.0.1",
    'password':"xiaorui.cc",
    'port':"3306",
    'database':'xiaorui',
}

class User(Model):
    table_name = 'user'
    debug = False
    db_config = db_config    

    name = CharField()
    addr = CharField()

if __name__ == "__main__":
    user = User()
    user.addr = "beijing of china"
    user.name = 'fengyun'
    user.save()
    user.addr = "shanghai of china"
    user.save()
    user.get(name='xiaorui.cc',addr="beijing")
