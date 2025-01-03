from django.db import models
from django.conf import settings


class Profile(models.Model):
    '''
    유저_ID, 이메일 인증 여부, 닉네임, 소개글, 플랫폼(로컬, 카카오 등)
    '''
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    email_verified = models.BooleanField(default=False)
    nickname = models.CharField(max_length=10)
    bio = models.TextField(max_length=50, blank=True)
    platform = models.CharField(max_length=10)
    
    class Meta:
        pass