from rest_framework import generics
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated

from django.contrib.auth import get_user_model

from user.serializer import CustomUserSerializer
User = get_user_model()

# Create your views here.


class UserWritePermission(BasePermission):
    message = 'Editing  is restricted to the author only.'

    def has_object_permission(self, request, view, obj):

        return obj == request.user


class DetailUser(generics.RetrieveUpdateDestroyAPIView, UserWritePermission):
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, UserWritePermission]
