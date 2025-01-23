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
    author = UserSerializer(read_only=True) #외래키로 현재 활성화 되어있는 User와 1:다 연결한다는 뜻이고 client가 요청할 때는 작성하지 않아도 됨(읽기 전용)
    like_user = UserSerializer(many=True,read_only=True) #게시글에 좋아요 누른 사람들은 여러명 일 수 있으니까(many=true)
    comment_count = serializers.IntegerField(source="comment.count",read_only=True) #post에는 comment필드가 없기 때문에 soucre에서 역참조해서 가져옴
    like_count = serializers.IntegerField(source="like_user.count",read_only=True)

    class Meta:
        model = Post
        fields = "__all__"

    def to_representation(self, instance): #to_representation 함수는 요청에 대한 응답 데이터를 직렬화하고 출력할 때 사용하는데, author랑 like_user 필드는 보여주고 싶지 않아서 pop으로 제거
        ret = super().to_representation(instance)
        ret.pop("author")
        ret.pop("like_user")
        return ret
