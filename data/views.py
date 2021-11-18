from typing import OrderedDict
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from device.models import Device
from utils import get_filter_by_date

from .serializers import CitySerializer, CountrySerializer, DataSerializer, DistrictSerializer
from .models import City, Country, Data, District


class StandardResultsSetPagination(PageNumberPagination):
    """ Pagination to products """
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 50
    page_query_param = 'p'

    def get_paginated_response(self, data):
        return Response(OrderedDict([
            ('count', self.page.paginator.count),
            ('countItemsOnPage', self.page_size),
            ('total_pages', self.page.paginator.num_pages),
            ('current', self.page.number),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))


class DataAccessPermission(permissions.BasePermission):
    message = 'Get data not allowed.'

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated


class DataList(generics.ListCreateAPIView, DataAccessPermission):
    serializer_class = DataSerializer
    permission_classes = [DataAccessPermission]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        This view should return a list of
        """
        user = self.request.user
        device = self.request.query_params.get('device')
        filter_by = self.request.query_params.get('filter_by')
        time_threshold = get_filter_by_date(filter_by)
        if device is not None:
            obj = get_object_or_404(Device, pk=device)
            if obj.owner_id == user:
                return Data.objects.filter(device_id=obj, date_time__gt=time_threshold)
            raise PermissionDenied()
        return Data.objects.filter(device_id__owner_id=user, date_time__gt=time_threshold)


class DataListAll(generics.ListAPIView, DataAccessPermission):
    serializer_class = DataSerializer
    permission_classes = [DataAccessPermission]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        """
        This view should return a all list of Data objects. 
        """
        user = self.request.user
        device = self.request.query_params.get('device')
        if device is not None:
            obj = get_object_or_404(Device, pk=device)
            if obj.owner_id == user:
                return Data.objects.filter(device_id=obj).order_by('-date_time')
            raise PermissionDenied()
        return Data.objects.filter(device_id__owner_id=user).order_by('-date_time')


class DataDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DataSerializer
    queryset = Data.objects.all()


class CountryList(generics.ListAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class CountryDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()


class CityList(generics.ListAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class CityDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CitySerializer
    queryset = City.objects.all()


class DistrictList(generics.ListAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


class DistrictDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DistrictSerializer
    queryset = District.objects.all()


"""
- Vista de calidad por 1 hora, 6 horas, 24 horas, 1 semana, 1 mes
-   {
    datos: [
        {
            avg: 10,
            variacion: 0
        }, 
        {
            avg: 50,
            variacion: +40
        }
    ]    

"""
