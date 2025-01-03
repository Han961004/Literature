from django.contrib import admin
from django.urls import path

from accounts.views.login import LoginView
from accounts.views.logout import LogoutView
from accounts.views.user import *

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # accounts
    path('v1/accounts/create/', UserView.as_view()),
    path('v1/accounts/login/', LoginView.as_view()),
    path('v1/accounts/logout/', LogoutView.as_view()),
]
