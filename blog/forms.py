from django.contrib import auth
from django.contrib.auth.models import User
from django import forms
from .models import Post, Comment


# Create your forms here.
class PostForm(forms.ModelForm):
    title = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Post
        fields = (
            'title', 'content',
        )


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea, required=True)

    class Meta:
        model = Comment
        fields = ('content',)
