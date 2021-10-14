from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response

from .serializers import UserLoginSerializer, UserCreateSerializer


User = get_user_model()


class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status_code = status.HTTP_201_CREATED
        response = {
            'message': "User Registered Successfully"
        }
        return Response(response, status=status_code)
