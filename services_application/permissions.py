import logging

import redis
from django.conf import settings
from rest_framework import permissions, status
from rest_framework.response import Response

from services_application.models import User

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class IsWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff or request.user.is_superuser or request.user.is_worker))

"""


class IsWorker(permissions.BasePermission):
    def has_permission(self, request, view):
        session_id = request.COOKIES.get('session_id')
        if session_id is None:
            return False
        user_id = session_storage.get(session_id)
        user = User.objects.get(id=int(user_id))
        return bool(user and (user.is_staff or user.is_superuser or user.is_worker))
"""

class IsStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        session_id = request.COOKIES.get('session_id')
        if session_id is None:
            return False
        user_id = session_storage.get(session_id)
        user = User.objects.get(id=user_id)
        return bool(user and (user.is_staff or user.is_superuser))


class IsSuperUser(permissions.BasePermission):
    def has_permission(self, request, view):
        session_id = request.COOKIES.get('session_id')
        if session_id is None:
            return False
        user_id = session_storage.get(session_id)
        user = User.objects.get(id=user_id)
        return bool(user and user.is_superuser)
