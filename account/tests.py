from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from account.models import Follow, Profile

User = get_user_model()

class Tests(APITestCase):

    # 초기화 user1 & user2 생성
    def setUp(self):
        self.join_url = reverse('user_create')
        self.login_url = reverse('login')

        self.user1 = User.objects.create_user(email='user1@example.com', password='password123')
        self.user1.is_active = True
        self.user1.save()
        Profile.objects.create(user=self.user1, nickname='user1')

        self.user2 = User.objects.create_user(email='user2@example.com', password='password123')
        self.user2.is_active = True
        self.user2.save()
        Profile.objects.create(user=self.user2, nickname='user2')
    
    # 권한
    def authenticate(self):
        res = self.client.post(self.login_url, {"email": "user1@example.com", "password": "password123"})
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        token = res.data['token'] if 'token' in res.data else res.data['response']['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

    # 회원 가입 및 프로필 생성 성공
    def user_join_success(self):
        data = {"email": "new@example.com", "password": "newpassword123"}
        res = self.client.post(self.join_url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="new@example.com").exists())
    
    # 회원 가입 실패
    def user_join_fail(self):
        data = {"email": "user1@example.com", "password": "short"}
        res = self.client.post(self.join_url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    # 회원 정보 수정 성공(패스워드 변경)
    
    # 회원 탈퇴 성공
    def user_delete_success(self):
        self.authenticate()
        url = reverse('user_delete')
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)

    # 프로필 정보 수정 성공
    
    # 프로필 정보 수정 실패
    
    # 로그인 성공
    def login_success(self):
        data = {"email": "user1@example.com", "password": "password123"}
        res = self.client.post(self.login_url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("token", res.data['response'])

    # 로그인 실패
    def login_fail(self):
        data = {"email": "user1@example.com", "password": "wrongpass"}
        res = self.client.post(self.login_url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        
    # 팔로우 생성
    
    # 팔로우 조회 
    
    # 팔로우 삭제