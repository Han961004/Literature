FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# requirements가 안 바뀌면 캐시 유지해서 RUN pip install 설치가 생략
# COPY . . 만 쓰는 것보다 COPY requirements를 한번 해주는게 좋음
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

VOLUME /app

EXPOSE 8080

# runserver는 도커파일 / makemigrations, migrate는 컴포즈파일
# CMD python manage.py runserver 0.0.0.0:8000