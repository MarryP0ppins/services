import uuid

from django.db.models import Min, Max
from django.conf import settings
from django.http import HttpResponse

from rest_framework.decorators import api_view, action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework import viewsets, status
from rest_framework.views import APIView

from .models import Contract, Service, User
from .permissions import IsStaff, IsSuperUser
from .serializers import ContractSerializer, ServiceSerializer, LoginSerializer, RegistrationSerializer

import redis

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)


class ContractsViewSet(viewsets.ModelViewSet):
    serializer_class = ContractSerializer

    def get_permissions(self):
        if self.action in ['list']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsStaff]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Contract.objects.all().order_by('id')
        user_id = self.request.query_params.get('user_id')
        status = self.request.query_params.get('status')

        if status:
            queryset = queryset.filter(status=status)
        if user_id:
            queryset = queryset.filter(client_id=user_id)
        return queryset

    def list(self, request, *args, **kwargs):
        serializer = ContractSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Contract.objects.all()
        contract = get_object_or_404(queryset, pk=pk)
        serializer = ContractSerializer(contract)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        try:
            contract = Contract.objects.get(pk=pk)
        except Contract.DoesNotExist:
            return Response({'message': 'The contracts does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ContractSerializer(contract, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        try:
            self.get_queryset().delete()
        except Exception:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class ServicesViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer

    def get_permissions(self):
        if self.action in ['list', 'price_range']:
            permission_classes = [IsAuthenticatedOrReadOnly]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsStaff]
        else:
            permission_classes = [IsSuperUser]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        queryset = Service.objects.all().order_by('id')
        contracts_ids = Contract.objects.values('service')
        all_contracts = self.request.query_params.get('all')
        services_ids = self.request.query_params.get('services_ids')
        title = self.request.query_params.get('title')
        price_min = self.request.query_params.get('price_min')
        price_max = self.request.query_params.get('price_max')
        rating = self.request.query_params.get('rating')
        city = self.request.query_params.get('city')

        if all_contracts != 'true':
            queryset = Service.objects.exclude(id__in=contracts_ids).order_by('id')
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

    @action(detail=False, methods=['get'])
    def price_range(self, request):
        services = self.get_queryset()
        try:
            return Response(services.aggregate(price_min=Min('price'), price_max=Max('price')))
        except:
            return Response([], status=status.HTTP_404_NOT_FOUND)

    def list(self, request, *args, **kwargs):
        serializer = ServiceSerializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Service.objects.all()
        service = get_object_or_404(queryset, pk=pk)
        serializer = ServiceSerializer(service)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        try:
            service = Service.objects.get(pk=pk)
        except Service.DoesNotExist:
            return Response({'message': 'The services does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ServiceSerializer(service, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        try:
            self.get_queryset().delete()
        except Exception:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        user = User.objects.get(username=serializer.data.get('username'))
        random_key = str(uuid.uuid4())
        response.set_cookie(key='uid', value=random_key, httponly=True)
        session_storage.set(random_key, value=user.pk)
        return response


class RegistrationAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['post'])
def auth_logout(request):
    session_id = request.COOKIES.get('session_id')
    if session_id:
        session_storage.delete(session_id)
        response = HttpResponse('ok')
        response.delete_cookie('session_id')
        return response
    return HttpResponse('Unauthorized', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
