from django.db.models import Min, Max
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import User, Contract, Service
from rest_framework import viewsets
from .serializers import UserSerializer, ContractSerializer, ServiceSerializer

@api_view(['GET'])
def priceRange(request):
    return Response(Service.objects.aggregate(price_min=Min('price'), price_max=Max('price')))

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer

class ContractsViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer

    def get_queryset(self):
        queryset = Contract.objects.all().order_by('id')
        user_id = self.request.query_params.get('user_id')
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        if user_id:
            queryset = queryset.filter(id_client=user_id)
        return queryset


class ServicesViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer

    def get_queryset(self):
        queryset = Service.objects.all().order_by('id')
        services_ids = self.request.query_params.get('services_ids')
        title = self.request.query_params.get('title')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        rating = self.request.query_params.get('rating')
        city = self.request.query_params.get('city')

        if services_ids:
            queryset = queryset.filter(id__in=services_ids.split(','))
        if title:
            queryset = queryset.filter(title__contains=title)
        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if rating:
            queryset = queryset.filter(rating__in=rating.split(','))
        if city:
            queryset = queryset.filter(city__contains=city)
        return queryset

