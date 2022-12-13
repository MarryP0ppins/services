from .models import User, Contract, Service
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'first_name', 'last_name', 'sex', 'phone', 'email', 'date_of_registration', 'date_of_birth', 'img']


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract

        fields = ['id', 'id_client', 'id_service', 'duration', 'date_of_execution', 'date_of_signing', 'status']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service

        fields = ['id', 'id_user', 'title', 'description', 'price', 'rating', 'city']