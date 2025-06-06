from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password']

    def validate_email(self, value):
        value = value.lower() ## 이메일 전부 소문자로
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("비밀번호는 최소 8자리 이상이어야 합니다.")
        return value

class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Profile
        fields = ['id', 'user', 'nickname', 'birth', 'bio']

    def validate_nickname(self, value):
        user = self.context['request'].user
        if Profile.objects.filter(nickname=value).exclude(user=user).exists():
            raise serializers.ValidationError("이미 사용 중인 닉네임입니다.")
        return value

class FollowSerializer(serializers.ModelSerializer):
    follower = serializers.PrimaryKeyRelatedField(read_only=True)
    following = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']

    def validate(self, data):
        follower = self.context['request'].user
        following = data['following']
        if follower == following:
            raise serializers.ValidationError("자기 자신을 팔로우할 수 없습니다.")
        if Follow.objects.filter(follower=follower, following=following).exists():
            raise serializers.ValidationError("이미 팔로우한 사용자입니다.")
        return data

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    token = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    profile = ProfileSerializer(read_only=True)

    def validate(self, data):
        email = data.get('email').lower() ## 이메일 소문자화
        password = data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError("유효하지 않은 로그인 정보입니다.")
        if not user.is_active:
            raise serializers.ValidationError("비활성화된 사용자입니다.")

        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        profile = user.profile
        
        data['response'] = {
            'user': UserSerializer(user).data,
            'profile': ProfileSerializer(profile).data,
            'token': token
        }
        return data
