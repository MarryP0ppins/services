from django.contrib import admin
from .models import Service, Contract, User


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'id', 'email', 'is_superuser', 'is_staff', 'is_worker')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    list_display = ('id', 'status')
