from gc import get_objects

from django.contrib.auth import login, get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import UserModel
from .serializers import UserSerializer,UserDetailSerializer,UserLoginSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView

# Create your views here.

class UserSignupView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self,request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            login(request,serializer.validated_data.get("user"))
            return Response({"message": "login successful."}, status=status.HTTP_200_OK)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(RetrieveUpdateDestroyAPIView):
    queryset = UserModel.objects.all()
    serializer_class = UserDetailSerializer

    def get_object(self):
        return get_object_or_404(UserModel,pk=self.kwargs['pk'])



