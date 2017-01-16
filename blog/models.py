from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import fields


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('accounts.User')
    title = models.CharField(max_length=255)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    # published_date = models.DateTimeField(blank=True, null=True)

    # def publish(self):
    #     self.published_date = timezone.now()
    #     self.save()

    # def approved_comments(self):
    #     return self.comments.filter(approved_comment=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Post: {title}>'.format(title=self.title)


class Comment(models.Model):
    author = models.ForeignKey('accounts.User')
    post = models.ForeignKey('blog.Post')
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    # approved_comment = models.BooleanField(default=False)

    # def approve(self):
    #     self.approved_comment = True
    #     self.save()

    def __str__(self):
        return self.text

    def __repr__(self):
        return '<Comment: {text}>'.format(text=self.text)
