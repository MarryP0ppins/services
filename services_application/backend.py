import redis
from django.conf import settings
from rest_framework import authentication, exceptions

from .models import User

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class RedisAuthentication(authentication.BaseAuthentication):

    def _authenticate_credentials(self, request, user_id, session_id):
        try:
            user = User.objects.get(pk=int(user_id))
        except User.DoesNotExist:
            msg = 'No user matching this token was found.'
            raise exceptions.AuthenticationFailed(msg)

        return user, session_id

    def authenticate(self, request):
        request.user = None

        try:
            session_id = request.COOKIES.get('session_id')
            if session_id is None:
                return None

            user_id = session_storage.get(session_id)
            if user_id is None:
                return None

            return self._authenticate_credentials(request, user_id, session_id)
        except:
            return None