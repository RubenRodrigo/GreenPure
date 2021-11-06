from rest_framework import serializers

from data.serializers import DataSerializer
from utils import get_filter_by_date
from .models import *


class DeviceSerializer(serializers.ModelSerializer):
    data_item = serializers.SerializerMethodField()

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
            'account_id',
            'activation_date',
            'state',
            'qr_code',
            'data_item',
        ]
