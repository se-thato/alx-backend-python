from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth.models import User

class CustomHeaderAuthentication(BaseAuthentication):
    # Custom authentication class that will authenticate users based on a custom header

    def authenticate(self, request):
        user_id = request.headers.get('X-USER-ID')
        if not user_id:
            return None

        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)