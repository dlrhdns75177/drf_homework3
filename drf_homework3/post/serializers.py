from rest_framework import serializers
from .models import Post,Comment
from user.serializers import UserSerializer

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField() #auther 필드에 해당하는 것들 다 보여주고 싶지 않아서 커스텀하기

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ('post','author')

    def get_author(self, obj):
        return obj.author.username  # author의 username만 반환


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    like_user = UserSerializer(many=True,read_only=True)
    comment_count = serializers.IntegerField(source="comment.count",read_only=True)
    like_count = serializers.IntegerField(source="like_user.count",read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret.pop("author")
        ret.pop("like_user")
        return ret
