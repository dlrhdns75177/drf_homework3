from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser #이미지를 포함한 데이터를 처리하기 위해서서
from . models import Profile
from . serializers import ProfileSerializer, UserSerializer

class SignupView(APIView):
    def post(self,request):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

class ProfileIntro(APIView):

    parser_classes = (MultiPartParser, FormParser)

    def get(self,request):
        profile = Profile.objects.get(user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = ProfileSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
