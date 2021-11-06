from django.core.exceptions import PermissionDenied
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from utils import get_filter_by_date
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
        fields = ['id', 'country']

    # def get_data_item(self, instance):
    #     request = self.context['request']
    #     user = request.user
    #     filter_by = request.query_params.get('filter_by')
    #     device = request.query_params.get('device')
    #     time_threshold = get_filter_by_date(filter_by)

    #     if device is not None:
    #         obj = get_object_or_404(Device, pk=device)
    #         if obj.account_id == user:
    #             ordered_queryset = instance.data.filter(
    #                 date_time__gt=time_threshold, device_id=device)
    #         raise PermissionDenied()
    #     else:
    #         ordered_queryset = instance.data.filter(
    #             date_time__gt=time_threshold)
    #     return DataSerializer(ordered_queryset, many=True, read_only=True).data


class CitySerializer(serializers.ModelSerializer):

    class Meta:
        model = City
        fields = ('id', 'city', 'country_id')


class DistrictSerializer(serializers.ModelSerializer):
    data = DataSerializer(many=True, read_only=True)

    class Meta:
        model = District
        fields = ('id', 'city_id', 'district', 'data', 'qualityAVG')
