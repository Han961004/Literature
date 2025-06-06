from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator


def send_verification_email(user):
    subject = "이메일 인증을 완료해주세요"
    message = f"안녕하세요 {user.email}님,\n\n이메일 인증을 위해 아래 링크를 클릭해주세요:\n\n" \
              f"http://localhost:8000/verify-email/{user.id}/"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

def send_password_reset_email(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    reset_url = f"http://localhost:8000/reset-password-confirm/{uid}/{token}/"

    subject = "비밀번호 재설정 안내"
    message = f"안녕하세요 {user.email}님,\n\n비밀번호 재설정을 위해 아래 링크를 클릭해주세요:\n\n{reset_url}"
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)
