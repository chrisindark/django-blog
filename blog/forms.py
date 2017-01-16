__author__ = 'christopherp'

from django.contrib import auth
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment

# Create your forms here.
class PostForm(forms.ModelForm):
    title = forms.CharField(required=True)
    text = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Post
        fields = (
            'title', 'text',
        )


class CommentForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Comment
        fields = ('text',)
