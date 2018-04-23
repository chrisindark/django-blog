from .models import User


class OAuthBackend(object):
    """OAuthBackend"""
    @staticmethod
    def authenticate(email=None):
        try:
            # Try to find a user matching the username provided
            user = User.objects.get(email=email)
            return user
        except User.DoesNotExist:
            user = User.objects.create_user(email=email)
            user.save()
            return user

    # Required for your backend to work properly - unchanged in most scenarios
    @staticmethod
    def get_user(user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
