## simple_orm_mysql

这是一个轻量级的mysql orm模型 ，目的是打造一个超级轻便的python orm， 现在只是把架子给搭建出来。

尽量让simple_orm_mysql的用法像django的orm ,这样能更加容易的上手

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
