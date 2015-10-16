## simple_orm_mysql

这是一个轻量级的mysql orm模型 ，目的是打造一个超级轻便的python orm， 现在只是把架子给搭建出来。

尽量让simple_orm_mysql的用法像django的orm ,这样能更加容易的上手

### To List:
1. query功能完善
    * User.where(id=123,name='fengyun').update(addr='bj')
    * User.where().count()
    * User.where().select()
    * User.where().select(order='id',order_method='DESC',limit=10)

2. 增加原生sql语句的支持

3. 路由(以后)

4. 缓存(以后)



example:

```

#coding:utf-8
from simple_orm_mysql import *

class User(Model):
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

```
