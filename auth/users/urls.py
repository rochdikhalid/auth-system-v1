from django.urls import path
from . import views
from .views import RegisterCustomUser, ResetPasswordRequest, LoginCustomUser, LogoutCustomUser



app_name = 'users'

urlpatterns = [
    path('register/', RegisterCustomUser.as_view(), name = 'register_user'),
    path('password-reset-request/', ResetPasswordRequest.as_view(), name = 'password-reset-request'),
    path('activate/<uidb64>/<token>/', views.activate, name = 'activate_mail'),
    path('password-reset/<uidb64>/<token>/', views.activate_reset, name = 'reset-activate'),
    path('login/', LoginCustomUser.as_view(), name = 'login'),
    path('logout/', LogoutCustomUser.as_view(), name = 'logout'),
]