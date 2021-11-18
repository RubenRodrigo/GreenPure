from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from device.models import Device
from device.serializer import DeviceDetailSerializer, DeviceSerializer
# Create your views here.


# Permissions
class DeviceUserWritePermission(BasePermission):
    message = 'Editing devices is restricted to the author only.'

    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user


class DeviceList(generics.ListCreateAPIView):
    serializer_class = DeviceDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Device.objects.filter(owner_id=user)

    def perform_create(self, serializer):
        serializer.save(owner_id=self.request.user)


class DeviceDetail(generics.RetrieveUpdateDestroyAPIView, DeviceUserWritePermission):
    queryset = Device.objects.all()
    serializer_class = DeviceDetailSerializer
    permission_classes = [IsAuthenticated, DeviceUserWritePermission]


class DeviceResumeDetail(generics.ListAPIView):
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Device.objects.filter(owner_id=user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deviceActivate(request, unique_id):
    """
    Receive an UUID, search the device and activates it  
    """
    if request.method == 'GET':
        user = request.user
        device = generics.get_object_or_404(
            Device, unique_id=unique_id)
        device.state = True
        device.owner_id = user
        device.save(update_fields=['state', 'owner_id'])
        return Response(status=status.HTTP_204_NO_CONTENT)
