from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from rest_framework import (
    generics,
    viewsets,
    status,
    response,
    permissions
)
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS
from django.contrib.auth import authenticate
from .serializer import UserSerializer, OwnerSerializer, DishSerializer
from .models import Owner, Dishes
import json


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

class IsUpdateProfile(permissions.BasePermission):

    def has_permission(self, request, view):
        # can write custom code
        print(view.kwargs, "Owner Check")
        try:
            user_profile = Owner.objects.get(
                pk=view.kwargs['Rpk'])
        except:
            return False

        if request.user.owner == user_profile:
            return True

        return False


class IsUniqueProfile(permissions.BasePermission):

    def has_permission(self, request, view):
        # can write custom code
        print(view.kwargs, "unique check")
        try:
            O1=request.user.owner
        except:
            return True
        return False

class RestaurantView(APIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    def get(self, request):
        owner = Owner.objects.all()[:64]
        data = OwnerSerializer(owner, many=True).data
        return response.Response(data)

    def post(self, request):
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class getOwnerRestro(APIView):
    # Using token only
    
    permission_classes = (IsAuthenticated,)
    
    def get(self, request):
        try:
            owner = Owner.objects.get(user=request.user)
        except:
            return response.Response({'error': 'INVALID USER'}, status=status.HTTP_404_NOT_FOUND)
        data = OwnerSerializer(owner).data
        return response.Response(data)


class RestaurantListView(generics.ListCreateAPIView):
    serializer_class=DishSerializer
    permission_classes = (IsUpdateProfile,IsAuthenticated, )
    def get_queryset(self):
        return Dishes.objects.filter(owner = get_object_or_404(Owner, pk=self.kwargs["pk"]))
    def post(self, request, pk):
        if request.user != Owner.objects.get(pk=pk).user:
            return response.Response({'error': 'user is not authorized to access this Restaurant'}, status=status.HTTP_403_FORBIDDEN)
        data = request.data
        serializer = DishSerializer(data=data)
        if serializer.is_valid():
            serializer.save(owner=Owner.objects.get(pk=pk))
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DishView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class=DishSerializer

class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserSerializer

    def post(self, request, format=None):
        print(request.data)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = ()

    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return response.Response({"token": user.auth_token.key, "restaurant": str(user.owner.pk)})
        else:
            return response.Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
