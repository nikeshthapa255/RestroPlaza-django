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
        # print(Dishes.objects.get(pk=view.kwargs['pk']))

        if request.user.owner == user_profile:
            return True

        return False


#restaurant get, post new restaurant

class RestaurantView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated | ReadOnly]
    serializer_class = OwnerSerializer
    queryset = Owner.objects.all()

    def get(self, request):
        owner = Owner.objects.all()[:64]
        data = OwnerSerializer(owner, many=True).data
        return response.Response(data)

    def post(self, request):
        print(request.data)
        print(dir(User.objects.get(pk=request.data.get("user"))))
        serializer = OwnerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)
        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# get restaurant by token
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


# User Create 
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

#Login User 
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


#Dishes post 
class DishView(generics.ListCreateAPIView):
    serializer_class= DishSerializer
    permission_classes= (IsAuthenticated, IsUpdateProfile)
    def get_queryset(self):
        return Dishes.objects.filter(owner_id=self.kwargs["Rpk"])

#Dish put , delete 
class DishDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class= DishSerializer
    permission_classes= (IsAuthenticated, IsUpdateProfile)
    def get_queryset(self):
        print(self.kwargs, "QUERY")
        return Dishes.objects.filter(pk=self.kwargs["pk"])

