from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post,Comment
from .serializers import PostSerializer,CommentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.conf import settings

class PostList(APIView):

    def permission(self):
        if self.request.method == "GET": 
            return [AllowAny()] #조회는 누구나 가능하지만
        elif self.request.method =="POST":
            return  [IsAuthenticated] #게시글 작성은 로그인 인증된 사람만 가능

    def get(self,request):
        post = Post.objects.all()
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True): #mtv djago에서 form을 만들었던 것처럼 serializer도 비슷한 역할(유효성을 검사를 통해서 serializers.py에서 정의한 필드와와 요청받은 data가 같은지 확인인)
            serializer.save(author=request.user) #PostSerializer에서 외래키인 author 필드를 연결을 해두었기 때문에 view에서 author 사용가능
            return Response(serializer.data,status=status.HTTP_201_CREATED) #주로 post에서 사용하는 201 status code는 요청을 잘 받았고, 새로운 리소스 잘 만들어서 응답 잘 보냈다
        
class PostDetail(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self,pk): #그냥 db에서 가져오는 것이기 때문에 requset가 필요하지 않음, 해당 class의 모든 메서드들이 중복되는 코드라서 따로 함수로 만들었다다
        return get_object_or_404(Post,pk=pk) #url로 들어온 데이터가 db에 있는지 확인해서 가져온다

    def get(self,request,pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self,request,pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post,data=request.data,partial=True) #수정하는 것이기 때문에 기본의 post 내용 db에서 가져오고 거기에 요청받은 내용으로 수정
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self,request,pk):
        post = self.get_object(pk)
        post.delete()
        return Response()
    
class CommentList(APIView):

    permission_classes = [IsAuthenticated]

    def get_object(self,pk):
        return get_object_or_404(Post,pk=pk)

    def get(self,request,pk):
        post = self.get_object(pk)
        comments = post.comment.all() #역참조해서 게시글에 있는 댓글들 모두 가져와와
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)
    
    def post(self,request,pk):
        post = self.get_object(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post,author=request.user) #Comment 모델에는 2개의 외래키가 있는데 이를 지정해줘야하니까 
            return Response(serializer.data)
        
class CommentDetail(APIView):

    permission_classes = [IsAuthenticated]

    def put(self,request,comment_pk):
        comment = get_object_or_404(Comment,pk=comment_pk) #이미 어떤 post인지는 comment 처음 작성할 때 지정이 되었기 때문에 comment객체만 가지고 commnet 수정가능
        serializer = CommentSerializer(comment,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save() #외래키는 최초의 객체를 생성할 때만 지정해주면 된다(이후에는 db에 저장되어 있는거 사용하면 되니까)
            return Response(serializer.data)
        
    def delete(self,request,comment_pk):
        comment = get_object_or_404(Comment,pk=comment_pk)
        comment.delete()
        return Response()

class LikeList(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request,pk):
        post = get_object_or_404(Post,pk=pk)
        check = request.user in post.like_user.all()
        return Response({"좋아하나요?": check})

    def post(self,request,pk):
        post = get_object_or_404(Post,pk=pk)
        if request.user in post.like_user.all():
            post.like_user.remove(request.user)
            return Response({"좋아요를 제거"})
        else:
            post.like_user.add(request.user)
            return Response({"좋아요를 추가"})
        
        