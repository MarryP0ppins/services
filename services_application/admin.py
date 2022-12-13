from django.contrib import admin
from .models import User, Service, Contract

admin.site.register(User)
admin.site.register(Service)
admin.site.register(Contract)