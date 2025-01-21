from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Post,Comment
from .serializers import PostSerializer,CommentSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings

class PostList(APIView):

    def get(self,request):
        post = Post.objects.all()
        serializer = PostSerializer(post,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(author=request.user)
            return Response(serializer.data,status=status.HTTP_200_OK)
        
class PostDetail(APIView):

    def get_object(self,pk): #그냥 db에서 가져오는 것이기 때문에 requset가 필요하지 않음
        return get_object_or_404(Post,pk=pk)

    def get(self,request,pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    def put(self,request,pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post,data=request.data,partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        
    def delete(self,request,pk):
        post = self.get_object(pk)
        post.delete()
        return Response()
    
class CommentList(APIView):

    def get_object(self,pk):
        return get_object_or_404(Post,pk=pk)

    def get(self,request,pk):
        post = self.get_object(pk)
        comments = post.comment.all()
        serializer = CommentSerializer(comments,many=True)
        return Response(serializer.data)
    
    def post(self,request,pk):
        post = self.get_object(pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(post=post)
            return Response(serializer.data)
        
class CommentDetail(APIView):

    def put(self,request,comment_pk):
        comment = get_object_or_404(Comment,pk=comment_pk)
        serializer = CommentSerializer(comment,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
    def delete(self,request,comment_pk):
        comment = get_object_or_404(Comment,pk=comment_pk)
        comment.delete()
        return Response()

class LikeList(APIView):

    def get(self,request,pk):
        post = get_object_or_404(Post,pk=pk)
        check = request.user in post.like_user.all()
        return Response({"좋아하나요?":check})

    def post(self,request,pk):
        post = get_object_or_404(Post,pk=pk)
        if request.user in post.like_user.all():
            post.like_user.remove(request.user)
            return Response({"좋아요를 제거"})
        else:
            post.like_user.add(request.user)
            return Response({"좋아요를 추가"})
        