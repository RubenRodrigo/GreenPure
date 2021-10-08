from rest_framework import serializers
from .models import *


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = ('id', 'device', 'account_id', 'activation_date', 'state')
