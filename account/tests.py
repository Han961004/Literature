from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from account.models import Profile

User = get_user_model()

class AccountTests(APITestCase):
    
    def setUp(self):
        self.user_data = {'email': 'test@example.com', 'password': 'password123'}
        self.user = User.objects.create_user(**self.user_data)
        self.user.is_active = True
        self.user.save()
        Profile.objects.create(user=self.user, nickname="tester")  # ✅ 프로필도 생성

    def test_user_signup(self):
        data = {'email': 'new@example.com', 'password': 'password123'}
        response = self.client.post(reverse('signup'), data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_login(self):
        response = self.client.post(reverse('login'), self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_read_profile(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_and_unfollow(self):
        other_user = User.objects.create_user(email='other@example.com', password='otherpass')
        Profile.objects.create(user=other_user, nickname='other')  # 다른 유저도 프로필 생성
        self.client.force_authenticate(user=self.user)
        response = self.client.post(reverse('follow-create'), {'following': other_user.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
