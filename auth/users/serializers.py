from django.contrib import auth
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import CustomUser



class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = CustomUser(
            email = validated_data['email'],
            username = validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ResetPasswordRequestSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length = 255)

class ResetPasswordSerializer(serializers. Serializer):

    password = serializers.CharField(max_length = 30)

class LoginSerializer(serializers.Serializer):

    email = serializers.EmailField(max_length = 255)
    password = serializers.CharField(max_length = 30, write_only = True)
    generated_tokens_for_user = serializers.SerializerMethodField()

    # To generate the access and refresh tokens for the authenticated user
    def get_generated_tokens_for_user(self, obj):
        user = CustomUser.objects.get(email = obj['email'])
        return {
            'refresh': user.generated_tokens_for_user()['refresh'],
            'access': user.generated_tokens_for_user()['access']
        }

    # To validate the attributes, then authenticate the user
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')
        user = auth.authenticate(email = email, password = password)
        if not user:
            raise AuthenticationFailed('Invalid credentials, try again')
        return {
            'email': user.email,
            'tokens': user.generated_tokens_for_user
        }
    
class LogoutSerializer(serializers.Serializer):

    default_error_messages = {
        'bad_refresh_token': ('Token is expired or invalid')
    }

    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.refresh_token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.refresh_token).blacklist()
        except TokenError:
            self.fail('bad_refresh_token')

    
