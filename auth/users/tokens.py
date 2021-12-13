from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import six



class TokenGenerator(PasswordResetTokenGenerator):

    # To hash user's primary key and user state for producing a token that is invalidated when it's used
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) +
            six.text_type(user.is_active)
        )
        
account_activation_token = TokenGenerator()

class ResetRequestTokenGenerator(PasswordResetTokenGenerator):
    
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.password) + six.text_type(user.times_password_changed) 
        )

reset_password_token = ResetRequestTokenGenerator()
