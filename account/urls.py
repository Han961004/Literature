from django.urls import path
from .views import *

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name='join'),
    path('user/', ReadUserView.as_view(), name='user'),
    path('user/update/', UpdateUserView.as_view()),
    path('user/delete/', DeleteUserView.as_view()),

    path('profile/', ReadProfileView.as_view(), name='profile'),
    path('profile/update/', UpdateProfileView.as_view()),

    path('follow/create', CreateFollowView.as_view(), name='following'),
    path('follow/', ReadFollowListView.as_view(), name='follow'),
    path('follow/delete/<int:pk>/', DeleteFollowView.as_view(), name='unfollowing'),

    path('login/', LoginView.as_view(), name='login'), 
    path('verify-email/<int:user_id>/', ConfirmEmailView.as_view()),
]
