from peewee import *

database = MySQLDatabase('activity', **{'host': 'localhost', 'user': 'activity', 'use_unicode': True, 'passwd': 'activity', 'charset': 'utf8', 'port': 3306})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Activity(BaseModel):
    activity_id = AutoField(column_name='activity_id')
    activity_img = CharField(constraints=[SQL("DEFAULT ''")])
    date = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    description = CharField()
    guests = CharField(constraints=[SQL("DEFAULT ''")])
    place = CharField()
    sort = CharField()
    stars = IntegerField(constraints=[SQL("DEFAULT 0")])
    tags = CharField()
    title = CharField()
    user_id = IntegerField(column_name='user_id')

    class Meta:
        table_name = 'activity'

class Registration(BaseModel):
    activity_id = IntegerField(column_name='activity_id')
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    email = CharField()
    gender = IntegerField(constraints=[SQL("DEFAULT 1")])
    name = CharField()
    phone = CharField()
    user_id = IntegerField(column_name='user_id')

    class Meta:
        table_name = 'registration'
        primary_key = False

class Star(BaseModel):
    activity_id = IntegerField(column_name='activity_id')
    user_id = IntegerField(column_name='user_id')

    class Meta:
        table_name = 'star'
        indexes = (
            (('activity', 'user'), True),
        )
        primary_key = False

class User(BaseModel):
    avatar_url = CharField(constraints=[SQL("DEFAULT ''")])
    email = CharField()
    gender = IntegerField(constraints=[SQL("DEFAULT 1")])
    name = CharField()
    password = CharField()
    phone = CharField()
    type = IntegerField(constraints=[SQL("DEFAULT 1")])
    user_id = AutoField(column_name='user_id')

    class Meta:
        table_name = 'user'

