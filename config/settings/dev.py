from .base import *

DEBUG = True

ALLOWED_HOSTS = ['*']  # 개발 중에는 모든 호스트 허용


# 개발용 PostgreSQL (Docker 컨테이너를 'db'로 실행 중이라고 가정)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'literature',
        'USER': 'postgres',
        'PASSWORD': '0000',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 콘솔에 이메일 출력 (실제 전송 X)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# 개발 환경에서는 보안 설정 완화 가능
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_CONTENT_TYPE_NOSNIFF = False
