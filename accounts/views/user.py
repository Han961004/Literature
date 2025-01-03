from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.user import User
from ..serializers.user import UserSerializer, UserCreateSerializer

class UserView(APIView):
    authentication_classes = []  # 인증 비활성화
    permission_classes = []      # 권한 검사 비활성화
    
    @staticmethod
    def get(request):
        '''
        유저 전체 리스트
        many=True는 직렬화 대상이 다수의 객체(QuerySet)임을 나타냄
        '''
        users = User.objects.all()
        return Response(UserSerializer(users, many=True).data)

    @staticmethod
    def post(request):
        '''
        create user / set_password() 에서 패스워드 암호화?
        '''
        serializer = UserCreateSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.save()
            user.set_password(serializer.validated_data['password'])
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserDetailView(APIView):
    
    @staticmethod
    def get(request, user_id):
        pass
    
    @staticmethod
    def put(request, user_id):
        pass
    
    @staticmethod
    def delete(request, user_id):
        pass