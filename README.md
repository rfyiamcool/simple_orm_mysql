## simple_orm_mysql

这是一个轻量级的mysql orm模型 ，目的是打造一个超级轻便的python orm， 现在只是把架子给搭建出来。

尽量让simple_orm_mysql的用法像django的orm ,这样能更加容易的上手。 我在博客中描述了开发orm框架的相关情况，有兴趣的朋友点进去看看 [http://xiaorui.cc/2015/10/16/%E5%A6%82%E4%BD%95%E5%BC%80%E5%8F%91%E5%BE%AE%E5%9E%8B%E7%9A%84python-orm%E6%A1%86%E6%9E%B6%E7%BC%93%E5%AD%98%E5%8F%8A%E8%B7%AF%E7%94%B1/](http://xiaorui.cc/2015/10/16/%E5%A6%82%E4%BD%95%E5%BC%80%E5%8F%91%E5%BE%AE%E5%9E%8B%E7%9A%84python-orm%E6%A1%86%E6%9E%B6%E7%BC%93%E5%AD%98%E5%8F%8A%E8%B7%AF%E7%94%B1/)


### To List:

加入了类变量清理,防止写入数据冲突

1. query功能完善
    * User.where(id=123,name='fengyun').update(addr='bj')
    * User.where().count()
    * User.where().select()
    * User.where(order_field='id',order_turn='DESC',limit=10).select()

2. 增加原生sql语句的支持

3. 路由(以后)

4. 缓存(以后)



example:

```

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
```
