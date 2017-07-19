from django import forms
from .models import Post
from .models import Comment


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
        model = Post
        fields = ('dateTime', 'title')
