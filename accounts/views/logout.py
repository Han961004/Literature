from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from ..models.user import User


class LogoutView(APIView):
    '''
    permission_classes 사용자 인증 여부를 확인하는 drf의 기본 권한 클래스
    permissions.IsAuthenticated가 인증되지 않은 사용자를 차단하며 401 반환
    '''
    permission_classes = [permissions.IsAuthenticated, ] 
    
    @staticmethod
    def get(request):
        '''
        remove API Token
        
        request.auth drf에서 인증된 사용자의 토큰을 나타냄
        Token.objects.get(key=request.auth) Token 모델에서 현재 사용자의 토큰을 검색
        
        204 No Content는 요청이 성공했음을 의미하며, 추가 데이터를 반환하지 않음
        토큰을 찾을 수 없으면 404 오류 반환
        '''
        token = get_object_or_404(Token, key=request.auth)
        token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)