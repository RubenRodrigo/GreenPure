from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions

from device.models import Device

from .serializers import CitySerializer, CountrySerializer, DataSerializer, DistrictSerializer
from .models import City, Country, Data, District


class DataAccessPermission(permissions.BasePermission):
    message = 'Get data not allowed.'

    def has_permission(self, request, view):
        if request.method == 'POST':
            return True
        return request.user and request.user.is_authenticated


class DataList(generics.ListCreateAPIView, DataAccessPermission):
    serializer_class = DataSerializer
    permission_classes = [DataAccessPermission]

    def get_queryset(self):
        """
        This view should return a list of
        """
        user = self.request.user
        device = self.request.query_params.get('device')
        if device is not None:
            obj = get_object_or_404(Device, pk=device)
            if obj.account_id == user:
                return Data.objects.filter(device_id=obj)
            raise PermissionDenied()
        return Data.objects.filter(device_id__account_id=user)


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
