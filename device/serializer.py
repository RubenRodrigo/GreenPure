from rest_framework import serializers

from data.serializers import DataSerializer
from .models import *


class DeviceSerializer(serializers.ModelSerializer):
    data = DataSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = [
            'id',
            'device',
            'account_id',
            'activation_date',
            'state',
            'data'
        ]
