from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated

from device.models import Device
from device.serializer import DeviceSerializer
from utils import get_filter_by_date
# Create your views here.


# Permissions
class DeviceUserWritePermission(BasePermission):
    message = 'Editing devices is restricted to the author only.'

    def has_object_permission(self, request, view, obj):

        return obj.account_id == request.user


class DeviceList(generics.ListCreateAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Device.objects.filter(account_id=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class DeviceDetail(generics.RetrieveUpdateDestroyAPIView, DeviceUserWritePermission):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, DeviceUserWritePermission]
