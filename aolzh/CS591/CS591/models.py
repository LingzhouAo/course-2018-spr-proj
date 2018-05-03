from django.db import models
import mongoengine
from mongoengine import *

class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

alex = User(email='aolzh@bu.edu', first_name='Alex', last_name='Ao').save()
