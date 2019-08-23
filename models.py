from peewee import *
from flask_login import UserMixin
from flask import request

import datetime

DATABASE = SqliteDatabase('shrubs7.sqlite')

class User(UserMixin, Model):
   username = CharField()
   email = CharField()
   password = CharField()

   class Meta:
      database = DATABASE
class Shrub(Model):
   detect_shrub = BooleanField()
   average_red = IntegerField()
   average_green = IntegerField()
   average_blue = IntegerField()
   image = CharField()
   location = CharField()
   description = TextField()
   author = ForeignKeyField(User, backref='shrubs')
   class Meta:
      database = DATABASE
def initialize():
   DATABASE.connect()
   DATABASE.create_tables([User, Shrub], safe=True)
   print("shrub TABLES CREATED")
   DATABASE.close()