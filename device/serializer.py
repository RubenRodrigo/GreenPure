from django.db.models.aggregates import Avg
from rest_framework import serializers

from data.serializers import DataSerializer
from utils import get_filter_by_date
from .models import *


class DeviceDetailSerializer(serializers.ModelSerializer):
    averages = serializers.SerializerMethodField()
    data_item = serializers.SerializerMethodField()

    def get_averages(self, instance):
        request = self.context['request']
        filter_by = request.query_params.get('filter_by')
        time_threshold = get_filter_by_date(filter_by)
        ordered_queryset = instance.data.filter(date_time__gt=time_threshold)
        quality = ordered_queryset.aggregate(value=Avg('quality'))
        humidity = ordered_queryset.aggregate(value=Avg('humidity'))
        temperature = ordered_queryset.aggregate(value=Avg('temperature'))
        warm = ordered_queryset.aggregate(value=Avg('warm'))
        concentration = ordered_queryset.aggregate(value=Avg('concentration'))
        averages = {
            "quality__avg": quality['value'],
            "humidity__avg": humidity['value'],
            "temperature__avg": temperature['value'],
            "warm__avg": warm['value'],
            "concentration__avg": concentration['value'],
        }
        return averages

    def get_data_item(self, instance):
        request = self.context['request']
        filter_by = request.query_params.get('filter_by')
        time_threshold = get_filter_by_date(filter_by)
        ordered_queryset = instance.data.filter(date_time__gt=time_threshold)
        return DataSerializer(ordered_queryset, many=True, read_only=True).data

    class Meta:
        model = Device
        fields = [
            'id',
            'device',
            'account_created_id',
            'owner_id',
            'activation_date',
            'unique_id',
            'state',
            'qr_code',
            'averages',
            'data_item',
        ]


class DeviceSerializer(serializers.ModelSerializer):
    averages = serializers.SerializerMethodField()

    def get_averages(self, instance):
        request = self.context['request']
        filter_by = request.query_params.get('filter_by')
        time_threshold = get_filter_by_date(filter_by)
        ordered_queryset = instance.data.filter(date_time__gt=time_threshold)
        quality = ordered_queryset.aggregate(value=Avg('quality'))
        humidity = ordered_queryset.aggregate(value=Avg('humidity'))
        temperature = ordered_queryset.aggregate(value=Avg('temperature'))
        warm = ordered_queryset.aggregate(value=Avg('warm'))
        concentration = ordered_queryset.aggregate(value=Avg('concentration'))
        averages = {
            "quality__avg": quality['value'],
            "humidity": humidity['value'],
            "temperature__avg": temperature['value'],
            "warm__avg": warm['value'],
            "concentration__avg": concentration['value'],
        }
        return averages

    class Meta:
        model = Device
        fields = [
            'id',
            'device',
            'account_created_id',
            'owner_id',
            'unique_id',
            'activation_date',
            'state',
            'qr_code',
            'averages'
        ]
