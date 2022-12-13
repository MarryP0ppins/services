from .models import User, Contract, Service
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['id', 'first_name', 'last_name', 'sex', 'phone', 'email', 'date_of_registration', 'date_of_birth']


class ContractSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contract

        fields = ['id', 'client_id', 'service_id', 'date_of_execution', 'date_of_signing', 'status']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service

        fields = ['id', 'user_id', 'title', 'duration', 'price', 'rating', 'city']