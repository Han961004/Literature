from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from account.models import Follow, Profile

User = get_user_model()

class Tests(APITestCase):

    def setUp(self):
        self.signup_url = reverse('join')
        self.login_url = reverse('login')
        self.follow_url = reverse('following')

        self.user = User.objects.create_user(email='user1@example.com', password='password123')
        self.user.is_active = True
        self.user.save()
        Profile.objects.create(user=self.user, nickname='user1')

        self.other_user = User.objects.create_user(email='user2@example.com', password='password123')
        self.other_user.is_active = True
        self.other_user.save()
        Profile.objects.create(user=self.other_user, nickname='user2')

    def test_user_signup(self):
        data = {
            "email": "new@example.com",
            "password": "newpassword123"
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email="new@example.com").exists())

    def test_user_login(self):
        data = {
            "email": "user1@example.com",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

    def test_follow_and_unfollow(self):
        # 로그인
        login_res = self.client.post(self.login_url, {
            "email": "user1@example.com",
            "password": "password123"
        })
        token = login_res.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        # follow
        res = self.client.post(self.follow_url, {"following": self.other_user.id})
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Follow.objects.filter(follower=self.user, following=self.other_user).exists())

        # unfollow
        follow_id = res.data['id']
        unfollow_url = reverse('unfollowing', kwargs={'pk': follow_id})
        del_res = self.client.delete(unfollow_url)
        self.assertEqual(del_res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Follow.objects.filter(id=follow_id).exists())
