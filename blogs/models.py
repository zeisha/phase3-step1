from django.db import models
from django.utils import timezone
from users.models import User


class Blog(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    blog_id = models.IntegerField(default=1)


class Post(models.Model):
    post_id = models.IntegerField(default=1)
    blog_id = models.IntegerField(default=1)
#   blog_id = models.ForeignKey(Blog, default=None, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    summary = models.TextField(default=None)
    text = models.TextField()
    dateTime = models.DateTimeField(
        default=timezone.now)

#   def publish(self):
    #   self.creation_date = timezone.now()

    def __str__(self):
        return self.title


class Comment(models.Model):
    user_id = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    post_id = models.IntegerField(default=1)
    blog_id = models.IntegerField(default=1)
    comment_id = models.IntegerField(default=1)
    text = models.TextField()
    dateTime = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.text

#   def publish(self):
    #   self.creation_date = timezone.now()
