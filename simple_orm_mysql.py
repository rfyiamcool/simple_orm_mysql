#coding:utf-8

class Model(object):
    def __init__(self, rid=0, **kwargs):
        self.table_name = self.__class__.__name__.lower()
        for name in self.field_names:
            field = getattr(self.__class__, name.replace("`", ""))
            setattr(self, name.replace("`", ""), field.default)
        for key, value in kwargs.items():
            setattr(self, key.replace("`", ""), value)
#        self.debug()

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

    def get_cursor(self):
        pass
        return None

    def insert(self):
        cu = self.get_cursor()

        field_names_sql = ", ".join(self.field_names)
        field_values_sql = ", ".join(self.field_values)

        sql = "insert into `%s`(%s) values(%s)" % (self.table_name, field_names_sql, field_values_sql)
        print sql

    def update(self):
        cu = get_cursor()

        name_value = []
        for name, value in zip(self.field_names, self.field_values):
            name_value.append("%s=%s" % (name, value))
        name_value_sql = ", ".join(name_value)

        sql = "update `%s` set %s where id = %d" % (self.table_name, name_value_sql, self.id)
        print sql

    def save(self):
        self.insert()

    def delete(self):
        cu = get_cursor()
        sql = "delete from `%s` where id = %d" % (self.table_name, self.id)
        print sql

    @classmethod
    def get(cls, **kwargs):
        query = Query(cls)
        return query.filter(**kwargs).first()

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

