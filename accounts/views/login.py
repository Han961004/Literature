from django.contrib.auth import authenticate, login
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from ..serializers.user import *


class LoginView(APIView):
    authentication_classes = []  # 인증 비활성화
    permission_classes = []      # 권한 검사 비활성화
    
    @staticmethod
    def post(request):
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.user
            login(request, user)
            return Response({"email": user.email, "token": serializer.get_token(user)}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
    