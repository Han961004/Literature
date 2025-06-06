from django.urls import path
from .views import *

urlpatterns = [
    path('user/create/', CreateUserView.as_view(), name='user_create'),
    path('user/', ReadUserView.as_view(), name='user_read'),
    path('user/update/', UpdateUserView.as_view(), name='user_update'),
    path('user/delete/', DeleteUserView.as_view(), name='user_delete'),

    path('profile/', ReadProfileView.as_view(), name='profile_read'),
    path('profile/update/', UpdateProfileView.as_view(), name='profile_update'),

    path('follow/create', CreateFollowView.as_view(), name='follow_create'),
    path('follow/', ReadFollowListView.as_view(), name='follow_read'),
    path('follow/delete/<int:pk>/', DeleteFollowView.as_view(), name='follow_delete'),

    path('login/', LoginView.as_view(), name='login'), 
    path('verify-email/<int:user_id>/', ConfirmEmailView.as_view()),
]
