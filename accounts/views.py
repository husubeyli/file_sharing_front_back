from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


from .serializers import UserLoginSerializer, UserCreateSerializer
from .models import UserInfo

User = get_user_model()
from rest_framework.authtoken.models import Token

class LoginView(TokenObtainPairView):
    serializer_class = UserLoginSerializer

    # def post(self, request, *args, **kwargs):
    #     serializer = self.serializer_class(data=request.data,
    #                                        context={'request': request})
    #     serializer.is_valid(raise_exception=True)
    #     user = serializer.validated_data['user']
    #     token, created = Token.objects.get_or_create(user=user)
    #     return super().post(request, *args, **kwargs)
    # def post(self, request, *args, **kwargs):
    #     response = super(LoginView, self).post(request, *args, **kwargs)
    #     token = Token.objects.get(key=response.data['access'])
    #     user_id = Token.objects.get(key=request.auth.key).user_id
    #     print(user_id, 'malas')
    #     return super().dispatch(request, *args, **kwargs)


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
