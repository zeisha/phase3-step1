from django import forms
from .models import Post
from .models import Comment
from .models import Blog


class SendPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'summary', 'text')


class SendCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('post_id', 'text')


class SearchForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('search',)
