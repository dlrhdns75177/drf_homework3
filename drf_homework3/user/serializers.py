from rest_framework import serializers
from .models import Profile
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}
        '''
        extra_kwargs 는 ModelSerializer에서 제공하는 메타 옵션으로 특정 필드의 세부 옵션을 추가할 때 사용
        client가 요청을 보낼때는 포함되어야하지만 client가 응답을 받을 때는 보이지 않음(쓰기 전용)
        '''

    def create(self, validated_data): #ModelSerializer에서 제공하는 create함수를 오버라이딩 기본적으로 create 함순느 validated_data를 사용하여 객체를 생성하고 저장
        password = validated_data.pop('password') 
        '''
        유효성 검사가 완료된 데이터들(validated_data=딕셔너리 형태) 중 password만 빼서 password라는 변수에 저장
        나머지 username이랑 email은 그대로 딕셔너리에 있음
        -> 비밀번호는 보안상의 이유로 해싱을 해서 따로 저장해야하니까
        '''
        User = get_user_model() #CustomUser 모델을 가져온다(단지 테이블만)
        user = User(**validated_data) #그리고 그 테이블에 validated_data와 매핑을 통해서 새 객체를 생성
        user.set_password(password)  # 비밀번호를 해싱(평뮨 말고 암호화한 문자열로 저장)
        user.save() #최정적으로 db에 저장
        return user

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ("user",)