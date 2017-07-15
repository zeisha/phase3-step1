from django.db import models
from django.contrib.auth.models import User


class User(User):
    default_blog_id = models.IntegerField(default=1)
    last_TOKEN = models.CharField(max_length=100, default="default")



