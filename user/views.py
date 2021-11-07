from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, BasePermission, IsAuthenticated
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

from user.serializer import CustomUserSerializer
User = get_user_model()

# Create your views here.


class UserWritePermission(BasePermission):
    message = 'Editing  is restricted to the author only.'

    def has_object_permission(self, request, view, obj):

        return obj == request.user


class DetailUser(generics.RetrieveUpdateDestroyAPIView, UserWritePermission):
    """ View to get, update or destroy. This action is only allowed to the author only """
    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, UserWritePermission]


class DetailCurrent(generics.RetrieveAPIView, UserWritePermission):
    """ View to get, update or destroy. This action is only allowed to the author only """
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated, UserWritePermission]

    def get_object(self):
        user = self.request.user
        return user


class CustomAccountCreate(APIView):
    """ View to create a custom account. Only allow post request"""
    permission_classes = [AllowAny]

    def post(self, request, format='json'):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
