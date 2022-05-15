from email.policy import default
from unicodedata import category
from django.db import models
import datetime
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=1000)
    body = models.TextField(max_length=10000)
    img = models.ImageField(upload_to="images/")
    date = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20)
    name = models.CharField(max_length=50)

class Comment(models.Model):
    body = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=50)
    value = models.IntegerField()