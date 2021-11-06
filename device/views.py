from rest_framework import generics
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

from device.models import Device
from device.serializer import DeviceSerializer
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
        serializer.save(account_id=self.request.user)


class DeviceDetail(generics.RetrieveUpdateDestroyAPIView, DeviceUserWritePermission):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [IsAuthenticated, DeviceUserWritePermission]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deviceActivate(request, device):
    if request.method == 'GET':
        user = request.user
        device = generics.get_object_or_404(
            Device, account_id=user, device=device)
        device.state = True
        device.save(update_fields=['state'])
        return Response(status=status.HTTP_204_NO_CONTENT)
