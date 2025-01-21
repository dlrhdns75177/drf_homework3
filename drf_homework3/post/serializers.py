from rest_framework import serializers
from .models import Post,Comment
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('post','author')


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_user = UserSerializer(many=True,read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("author")
        ret.pop("like_user")
        return ret
