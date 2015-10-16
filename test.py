#coding:utf-8
from simple_orm_mysql import *

class User(Model):
    table_name = 'user'
    debug = False
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
