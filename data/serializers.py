from rest_framework import serializers
from .models import *


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Data
        fields = ('__all__')


class CountrySerializer(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = ('id', 'country')


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'city', 'country_id')


class DistrictSerializer(serializers.ModelSerializer):
    data = DataSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = ('id', 'city_id', 'district', 'data', 'qualityAVG')
