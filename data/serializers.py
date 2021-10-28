from rest_framework import serializers
from .models import *


class DataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Data
        fields = [
            "id",
            "district_id",
            "device_id",
            "latitude",
            "longitude",
            "quality",
            "date_time",
            "humidity",
            "temperature",
            "warm",
            "concentration",
            "smoke_sensor",
            "methane_sensor",
            "difference_quality",
        ]

    def validate_device_id(self, value):
        if value.state is False:
            raise serializers.ValidationError("This device is not available")
        return value

    def create(self, validated_data):
        data = self.context['request'].data
        country, created = Country.objects.get_or_create(
            country=data['country'])
        city, created = City.objects.get_or_create(
            city=data['city'], country_id=country)
        district, created = District.objects.get_or_create(
            district=data['district'], city_id=city)
        return Data.objects.create(district_id=district, **validated_data)


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
