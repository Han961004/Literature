from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from ..models.user import User
from ..models.profile import Profile


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'

class UserCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = '__all__'
        
    def create(self, validated_data):
        '''
        User와 연관된 Profile 생성 및 패스워드 암호화
        '''
        validated_data['password'] = make_password(validated_data['password'])  # 비밀번호 암호화
        user = super().create(validated_data)
        Profile.objects.create(user=user, nickname=validated_data.get('nickname', 'Default'), platform='web')
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['email', 'password', 'token']
    
    def validate(self, data):
        '''
        email 과 password로 사용자 인증
        '''
        user = authenticate(email=data['email'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        self.user = user
        return data
    
    @staticmethod
    def get_token(user):
        '''
        get or create token
        '''
        token, created = Token.objects.get_or_create(user=user)
        return token.key