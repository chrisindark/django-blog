from django.contrib import admin
from .models import Post, Comment


# Register your models here.
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text', 'created_date',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'post', 'text', 'created_date',)

admin.site.register(Post)
admin.site.register(Comment)
