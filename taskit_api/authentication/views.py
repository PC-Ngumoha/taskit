from authentication.serializers import (
    UserRegisterSerializer, UserLoginSerializer)
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class UserRegisterView(GenericAPIView):
    authentication_classes = []
    serializer_class = UserRegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(GenericAPIView):
    authentication_classes = []
    serializer_class = UserLoginSerializer

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(username=email, password=password)

        if user:
            serializer = self.serializer_class(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({"message": "Invalid Credentials, please try again"},
                        status=status.HTTP_404_NOT_FOUND)


class AuthUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        serializer = self.serializer_class(request.user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)
