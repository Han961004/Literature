import logging
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiResponse
from rest_framework.exceptions import APIException

from .models import Profile
from .serializers import *
from account.services import send_verification_email


logger = logging.getLogger(__name__)
User = get_user_model()

@extend_schema_view(
    post=extend_schema(
        summary='회원(user) 생성, 회원(profile) 생성',
        description='회원 생성 후(db는 생성, is_active=false) 이메일 인증을 보냄, 프로필은 자동으로 생성하므로 트랜잭션화',
        responses={
            201: UserSerializer,
            400: OpenApiResponse(description="클라이언트 에러 - serializer validate Error"),
            500: OpenApiResponse(description="서버 에러 - db Error or etc.")
        }
    )
)
class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        try:
            with transaction.atomic():
                validated_data = serializer.validated_data
                user = User.objects.create_user(email=validated_data['email'], password=validated_data['password'])
                Profile.objects.create(user=user, nickname=f"user_{user.id}") ## 기본 닉네임 user_0000
                send_verification_email(user) ## 이메일 보내고 확인하면 is_active=true로 활성화
        except Exception as e:
            logger.exception(e)
            raise APIException("서버 에러")

@extend_schema_view(
    get=extend_schema(
        summary='회원(user) 단일 조회',
        description='타인의 마이 페이지 조회',
        responses={
            200: UserSerializer,
            401: OpenApiResponse(description="클라이언트 에러 - no permission"),
            404: OpenApiResponse(description="클라이언트 에러 - user not exist")
        }
    )
)
class ReadUserView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    patch=extend_schema(
        summary='회원(user) 수정',
        description='Password를 받아 패스워드 수정',
        responses={200: UserSerializer}
    )
)
class UpdateUserView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']  # PATCH만 허용

    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        serializer.save()

@extend_schema_view(
    delete=extend_schema(
        summary='회원(user) 탈퇴',
        description='회원 탈퇴',
        responses={204: OpenApiResponse(description='회원 탈퇴 성공')}
    )
)
class DeleteUserView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

@extend_schema_view(
    get=extend_schema(
        summary='회원(profile) 단일 조회',
        description='현재 로그인한 사용자의 프로필을 조회합니다.',
        responses={
            200: ProfileSerializer,
            401: OpenApiResponse(description="인증이 필요합니다."),
            404: OpenApiResponse(description="프로필이 존재하지 않습니다.")
        }
    )
)
class ReadProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

@extend_schema_view(
    patch=extend_schema(
        summary='회원(profile) 수정',
        description='현재 로그인한 사용자의 프로필을 수정합니다.',
        responses={
            200: ProfileSerializer,
            400: OpenApiResponse(description="입력값이 유효하지 않습니다."),
            401: OpenApiResponse(description="인증이 필요합니다.")
        }
    )
)
class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch']

    def get_object(self):
        return self.request.user.profile

@extend_schema(
    summary="회원 팔로우(follow) 생성",
    description="다른 유저를 팔로우합니다. 이미 팔로우 중이거나 자신을 팔로우하려 하면 오류가 발생합니다.",
    responses={
        201: FollowSerializer,
        400: OpenApiResponse(description="유효하지 않은 요청입니다. (자기 자신을 팔로우하거나 중복된 팔로우)"),
        403: OpenApiResponse(description="인증이 필요한 요청입니다."),
        500: OpenApiResponse(description="서버 내부 오류"),
    }
)
class CreateFollowView(generics.CreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(follower=self.request.user)

    
@extend_schema(
    summary="회원 팔로우(follow) 목록 조회",
    description="팔로잉 또는 팔로워 목록을 조회합니다. 쿼리 파라미터 `type`은 `following` 또는 `follower` 중 하나입니다.",
    responses={
        200: FollowSerializer(many=True),
        400: OpenApiResponse(description="쿼리 파라미터가 잘못되었거나 값이 누락됨"),
        403: OpenApiResponse(description="인증이 필요한 요청입니다."),
    }
)
class ReadFollowListView(generics.ListAPIView):
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        t = self.request.query_params.get('type')
        if t == 'following':
            return Follow.objects.filter(follower=user)
        elif t == 'follower':
            return Follow.objects.filter(following=user)
        return Follow.objects.none()

@extend_schema(
    summary="회원 팔로우(follow) 삭제",
    description="팔로우 관계를 삭제합니다. 주어진 ID의 팔로우 객체를 삭제합니다.",
    responses={
        204: OpenApiResponse(description="삭제 성공"),
        403: OpenApiResponse(description="인증이 필요한 요청입니다."),
        404: OpenApiResponse(description="팔로우 관계를 찾을 수 없습니다."),
        500: OpenApiResponse(description="서버 내부 오류"),
    }
)
class DeleteFollowView(generics.DestroyAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated]

@extend_schema_view(
    post=extend_schema(
        summary='회원 로그인(login)',
        description='이메일 및 패스워드 입력 후 로그인 -> user, profile, token을 반환',
        responses={
            200: UserSerializer,
            400: OpenApiResponse(description="클라이언트 에러 - mail/password incorrect or not verified"),
            500: OpenApiResponse(description="서버 에러")
        }
    )
)
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data['response'], status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema_view(
    get=extend_schema(
        summary='이메일 인증 확인',
        description='user_id를 받아 이메일 인증 상태를 확인하고 활성화합니다.',
        responses={
            200: OpenApiResponse(description="이메일 인증 성공 또는 이미 인증됨"),
            404: OpenApiResponse(description="해당 ID의 사용자가 존재하지 않습니다.")
        }
    )
)
class ConfirmEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        if not user.is_active:
            user.is_active = True
            user.save()
            return Response({"message": "이메일 인증이 완료되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "이미 인증된 계정입니다."}, status=status.HTTP_200_OK)
