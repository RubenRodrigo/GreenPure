from rest_framework import generics

from .serializers import CitySerializer, CountrySerializer, DataSerializer, DistrictSerializer
from .models import City, Country, Data, District


class DataList(generics.ListCreateAPIView):
    serializer_class = DataSerializer
    queryset = Data.objects.all()


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
