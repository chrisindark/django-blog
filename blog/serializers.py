from rest_framework import serializers

from .models import Post
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True, required=False)
    username = serializers.EmailField(read_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'created_at', 'updated_at',)
        read_only_fields = ('created_at', 'updated_at',)


class PostSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True, required=False)

    class Meta:
        model = Post
        fields = ('title', 'text', 'amount', 'created_at', 'updated_at', 'user')
        read_only_fields = ('created_at', 'updated_at',)