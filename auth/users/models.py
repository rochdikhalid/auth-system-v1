from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from rest_framework_simplejwt.tokens import RefreshToken



# To set the custom user model
class CustomUserManager(BaseUserManager):

    def create_user(self, email, username, password = None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email = self.normalize_email(email),
            username = username
        )
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, email, username, password = None):
        user = self.create_user(
            email,
            password = password,
            username = username,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using = self._db)
        return user
                  
class CustomUser(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField(max_length = 255, unique = True)
    username = models.CharField(max_length = 150, unique = True)
    is_active = models.BooleanField(default = False)
    is_admin = models.BooleanField(default = False)
    times_password_changed = models.IntegerField(default = 0)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # Object string representation
    def __str__(self):
        return self.email

    # Correct plural
    class Meta: 
        verbose_name_plural = 'users'

    @property
    def is_staff(self):
        return self.is_admin

    # The generated tokens when the user logs in
    def generated_tokens_for_user(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

