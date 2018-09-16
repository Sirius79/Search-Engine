from django.db import models
from mongoengine import Document, EmbeddedDocument, fields
from mongo_connection import *



class Tool(Document):
    keyword = fields.StringField(required=True)
    count = fields.ListField(required=True)
    links = fields.ListField(required=True)

# Create your models here.
