import django_filters
from .models import *


class PostFilter(django_filters.FilterSet):
    class Meta:
        model = Post
        fields = (
            'author__username',
            'created_date',
        )
        order_by = (
            'created_date',
            '-created_date',
        )


class CommentFilter(django_filters.FilterSet):
    class Meta:
        model = Comment
        fields = (
            'post__id',
            'created_date',
        )
        order_by = (
            'created_date',
            '-created_date',
        )

# class FileUploadFilter(django_filters.FilterSet):
    # class Meta(PostFilter.Meta):
        # model = FileUpload
