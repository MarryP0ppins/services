from .models import User, Contract, Service
from rest_framework import viewsets
from .serializers import UserSerializer, ContractSerializer, ServiceSerializer

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

class ContractsViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer

    def get_queryset(self):
        queryset = Contract.objects.all().order_by('id')
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class ServicesViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.all().order_by('id')
        title = self.request.query_params.get('title')
        duration_min = self.request.query_params.get('duration_min')
        duration_max = self.request.query_params.get('duration_max')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        rating = self.request.query_params.get('rating')
        city = self.request.query_params.get('city')
        if title:
            queryset = queryset.filter(title__contains=title)
        if duration_min:
            queryset = queryset.filter(duration__gte=duration_min)
        if duration_max:
            queryset = queryset.filter(duration__lte=duration_max)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if rating:
            queryset = queryset.filter(rating__in=rating.join(''))
        if price_max:
            queryset = queryset.filter(city__contains=city)
        return queryset

