from peewee import *
from flask_login import UserMixin
from flask import request
from playhouse.db_url import connect 

import datetime
import os

DATABASE = connect(os.environ.get('DATABASE_URL'))

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
   height = IntegerField()
   width = IntegerField()
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
