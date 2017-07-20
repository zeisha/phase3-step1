from django.db import models
from django.utils import timezone
from users.models import User


class Blog(models.Model):
    user = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    blog_id = models.IntegerField(default=1)
    posts_words = models.CharField(default="", max_length=1000)
    wordcount = {}
    score = models.IntegerField(default=0)
    search = models.CharField(default="", max_length=100)

    def count_words(self):
        self.posts_words = ""
        posts = Post.objects.filter(blog_id=self.blog_id)
        for post in posts:
            words = post.text.split()
            for word in words:
                if word not in self.wordcount:
                    self.wordcount[word] = 1
                else:
                    self.wordcount[word] += 1
        for word in self.wordcount:
            self.posts_words += word
            self.posts_words += "-"
            self.posts_words += self.wordcount[word]
            #check the word isn't the last one
            self.posts_words += ","



class Post(models.Model):
    post_id = models.IntegerField(default=1)
    blog_id = models.IntegerField(default=1)
    title = models.CharField(max_length=200)
    summary = models.TextField(default=None)
    text = models.TextField()
    dateTime = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.title


class Comment(models.Model):
    #user_id = models.ForeignKey(User, default=None, on_delete=models.CASCADE)
    post_id = models.IntegerField(default=1)
    blog_id = models.IntegerField(default=1)
    comment_id = models.IntegerField(default=1)
    text = models.TextField()
    dateTime = models.DateTimeField(
        default=timezone.now)

    def __str__(self):
        return self.text
