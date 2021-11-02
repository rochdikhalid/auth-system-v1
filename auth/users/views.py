from rest_framework import status
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CustomUserSerializer, ResetPasswordRequestSerializer, ResetPasswordSerializer, LoginSerializer, LogoutSerializer
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token, reset_password_token
from .models import CustomUser


# The register view
class RegisterCustomUser(APIView):

    def get(self, request):
        return Response(reverse_lazy('users:register_user'))

    def post(self, request, format = 'json'):
        serializer = CustomUserSerializer(data = request.data)
        # To verify the credentials
        if serializer.is_valid():
            user = serializer.save()
            json = serializer.data
            user_email = CustomUser.objects.get(email = json['email'])
            # Setting mail dependencies
            current_site = get_current_site(request).domain
            mail_subject = 'Activate your blog account.'
            message = render_to_string('activate_mail.html', {
                'user': user,
                'domain': current_site,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            # To send the mail
            send_mail(mail_subject, message, 'me@example.com', [user_email], fail_silently = False)
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# The reset password request view
class ResetPasswordRequest(APIView):

    def get(self, request):
        return Response(reverse_lazy('users:password-reset-request'))

    def post(self, request, format = 'json'):
        serializer = ResetPasswordRequestSerializer(data = request.data)
        # To verify the credentials
        if serializer.is_valid():
            json = serializer.data            
            current_site = get_current_site(request).domain
            mail_subject = 'Reset your password'
            # To throw an error when user's email is not existed
            try:
                user_email = CustomUser.objects.get(email = json['email'])
            except(CustomUser.DoesNotExist):
                user_email = None
                return Response('Email does not exist', status = status.HTTP_400_BAD_REQUEST)  
            # To send the mail to the user's email when it's existed  
            if user_email is not None:
                # Setting mail dependencies
                message = render_to_string('reset_request.html', {
                    'user': user_email,
                    'domain': current_site,
                    'uid':urlsafe_base64_encode(force_bytes(user_email.pk)),
                    'token':reset_password_token.make_token(user_email),
                })
                # To send the mail
                send_mail(mail_subject, message, 'me@example.com', [user_email], fail_silently = False)
                return Response('Check you email, we sent a link to reset your password.')  
            return Response('Email does not exist')
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

# Email confirmation view
@api_view(('GET',))
def activate(request, uidb64, token):
    # To throw an error in case if the user is not existed
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    # To set the user's status when the email is activated
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return Response('Thank you for your email confirmation. Now you can login your account.')
    else:
        return Response('Activation link is invalid!')

# Reset password activation
@api_view(('GET', 'POST',))
def activate_reset(request, uidb64, token, format = 'json'):
    # To throw an error in case if the user is not existed
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk = uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    # To activate the reset password link so the user can reset the password
    if user is not None and reset_password_token.check_token(user, token):
        serializer = ResetPasswordSerializer(data = request.data)
        if serializer.is_valid():
            json = serializer.data
            user.set_password(json['password'])
            user.times_password_changed += 1
            user.save()         
            return Response('Your password changed successfully, you can login now.')
        else:
            return Response(serializer.errors)
    return Response('Token is invalid! try again', status = status.HTTP_400_BAD_REQUEST)

# The login view
class LoginCustomUser(APIView):

    def get(self, request):
        return Response(reverse_lazy('users:login'))

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        # To verify the credentials
        if serializer.is_valid():
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.errors, status = status.HTTP_401_UNAUTHORIZED)
        
# The logout view
class LogoutCustomUser(APIView):

    def get(self, request):
        return Response(reverse_lazy('users:logout'))

    def post(self, request):
        serializer = LogoutSerializer(data = request.data)
        # To verify the credentials
        if serializer.is_valid():
            serializer.save()
        return Response(serializer.errors, status = status.HTTP_204_NO_CONTENT)


