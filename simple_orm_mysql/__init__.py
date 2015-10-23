#coding:utf-8
from simple_orm_mysql.store import SqlStore
from simple_orm_mysql.store import *

class Utils(object):
   def join_where(self,kwargs): 
        str_list = []
        index = 0
        for i in kwargs.iteritems():
            if not index == len(kwargs):
                str = "%s=%s"%(i[0],i[1])
                str_list.append(str)
                index +=1
        where_sql = ' and '.join(str_list)        
        return where_sql

class Syntax(object):
    def __init__(self, model, kwargs):
        self.model = model
        self.params = kwargs.values()
        equations = [key + ' = %s' for key in kwargs.keys()]
        self.where_expr = 'where ' + ' and '.join(equations) if len(equations) > 0 else ''

    def update(self, **kwargs):
        _keys = []
        _params = []
        for key, val in kwargs.iteritems():
            if val is None or key not in self.model.fields:
                continue
            _keys.append(key)
            _params.append(val)
        _params.extend(self.params)
        sql = 'update %s set %s %s;' % (
            self.model.table_name, ', '.join([key + ' = %s' for key in _keys]), self.where_expr)
        return sql, _params

    def limit(self, rows, offset=None):
        self.where_expr += ' limit %s%s' % (
            '%s, ' % offset if offset is not None else '', rows)
        return self

    def select(self):
        sql = 'select %s from %s %s;' % (', '.join(self.model.fields.keys()), self.model.table_name, self.where_expr)
        for row in Database.execute(sql, self.params).fetchall():
            inst = self.model()
            for idx, f in enumerate(row):
                setattr(inst, self.model.fields.keys()[idx], f)
            yield inst

    def count(self):
        sql = 'select count(*) from %s %s;' % (self.model.table_name, self.where_expr)
        (row_cnt, ) = Database.execute(sql, self.params).fetchone()
        return row_cnt

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        print cls,name,bases,attrs
        print attrs['Meta'].database
        print('Found model: %s' % name)
        mappings = dict()
        for k, v in attrs.iteritems():
            if isinstance(v, Field):
                print('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
        for k in mappings.iterkeys():
            attrs.pop(k)
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = name # 假设表名和类名一致
        return type.__new__(cls, name, bases, attrs)

class Model(Utils):
    __metaclass__ = ModelMetaclass
    def __init__(self, rid=0, **kwargs):
        if not getattr(self.__class__,'table_name'):
            self.table_name = self.__class__.__name__.lower()
        if getattr(self.__class__,'db_config'):
            self.db_config = getattr(self.__class__,'db_config') 
        else:
            raise NotFindArgv('not find db_config argv')
        for name in self.field_names:
            field = getattr(self.__class__, name.replace("`", ""))
            setattr(self, name.replace("`", ""), field.default)
        for key, value in kwargs.items():
            setattr(self, key.replace("`", ""), value)
        if getattr(self.__class__,'debug'):
            self.debug()
        self.build_conn()

    def build_conn(self):
        self.sqlstore = SqlStore(**self.db_config)
        self.cursor = self.sqlstore.get_cursor()
        
    def debug(self):
        for name in dir(self.__class__):
            print name,'-------',getattr(self.__class__,name)

    @property
    def field_names(self):
        names = []
        for name in dir(self.__class__):
            var = getattr(self.__class__, name.replace("`", ""))
            if isinstance(var, Field):                
                names.append("`%s`"%name)
        return names

    @property
    def field_values(self):
        values = []
        for name in self.field_names:
            value = getattr(self, name.replace("`", ""))
            if isinstance(value, Model):
                value = value.id
            if isinstance(value, str):
                value = value.replace("'", "''")
                try:
                    value = value.decode("gbk")
                except Exception, e:
                    pass
                try:
                    value = value.decode("utf8")
                except Exception, e:
                    pass
            values.append("'%s'" % value)
        return values

    def insert(self):
        field_names_sql = ", ".join(self.field_names)
        field_values_sql = ", ".join(self.field_values)

        sql = "insert into '%s'(%s) values(%s)" % (self.table_name, field_names_sql, field_values_sql)
        return self.cursor.execute(sql)

    def update(self):
        name_value = []
        for name, value in zip(self.field_names, self.field_values):
            name_value.append("%s=%s" % (name, value))
        name_value_sql = ", ".join(name_value)

        sql = "update `%s` set %s where id = %d" % (self.table_name, name_value_sql, self.id)
        return self.cursor.execute(sql)

    def save(self):
        self.insert()

    def delete(self, **kwargs):
        where_sql = self.join_where(kwargs)
        sql = "delete from %s where %s"%(self.table_name,where_sql)
        return self.cursor.execute(sql)

    def get(self, **kwargs):
        where_sql = self.join_where(kwargs)
        sql = "select * from %s where %s"%(self.table_name,where_sql)
        return self.cursor.execute(sql)

    def where(self, **kwargs):
        return Syntax(self, kwargs)

class Field(object):
    field_type = ""
    field_level = 0
    default = ""

    def field_sql(self, field_name):
        return '"%s" %s' % (field_name, self.field_type)

class CharField(Field):
    def __init__(self, max_length=255, default=""):
        self.field_type = "varchar(%d)" % max_length
        self.default = default
        self.max_length = max_length

class IntField(Field):
    def __init__(self, default=None):
        self.default = default

def ValidField(max_length):
    if max_length > 255:
        raise FieldError('max_lenth lt 255')

