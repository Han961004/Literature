# config/settings/__init__.py에 아래와 같이 설정해두면 기본 환경 자동 지정도 가능:

import os
env = os.getenv("DJANGO_ENV", "dev")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"config.settings.{env}")
