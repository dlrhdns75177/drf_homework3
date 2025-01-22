from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}} #client가 요청을 보낼때는 포함되어야하지만 client가 응답을 받을 때는 보이지 않음(쓰기 전용)

    def create(self, validated_data):
        password = validated_data.pop('password') 
        '''
        유효성 검사가 완료된 데이터들 중(딕셔너리) password만 빼서 password라는 변수에 저장
        나머지 username이랑 email은 그대로 딕셔너리에 있음
        -> 비밀번호는 보안상의 이유로 해싱을 해서 따로 저장해야하니까
        '''
        User = get_user_model()
        user = User(**validated_data)
        user.set_password(password)  # 비밀번호를 해싱
        user.save() #그리고 저장
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("user",)