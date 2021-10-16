import json
from django.contrib.auth import get_user_model

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from .models import UserInfo
from .utils import get_ip_adress


User = get_user_model()




class UserLoginSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        context = {}
        request =  self.context['request']
        user_data = UserSerializer(self.user).data
        data.update(**user_data)
        user = self.user
        # user_info, created = UserInfo.objects.get_or_create(browser_family='ISO', user_id=user.id, username=user.username)
        try:
            user_info = UserInfo.objects.using('users_db').get(
                browser_family=request.user_agent.browser.family, 
                user_id=user.id, 
                username=user.username,
                browser_version=request.user_agent.browser.version_string,
                os_family=request.user_agent.os.family,
                os_version=request.user_agent.os.version_string,
                ip_adress=get_ip_adress(request)
            )
        except UserInfo.DoesNotExist:
            user_info = UserInfo.objects.using('users_db').create(
                browser_family=request.user_agent.browser.family, 
                user_id=user.id, 
                username=user.username,
                browser_version=request.user_agent.browser.version_string,
                os_family=request.user_agent.os.family,
                os_version=request.user_agent.os.version_string,
                ip_adress=get_ip_adress(request)
            )

        context['data'] = data
        context['user'] = user
        
        return data

    


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(
        queryset=User.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])

    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'
        ]
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})

        return attrs

    def create(self, validate_data):
        user = User.objects.create(
            username=validate_data['username'],
            email=validate_data['email'],
            first_name=validate_data['first_name'],
            last_name=validate_data['last_name']
        )
        user.set_password(validate_data['password'])
        user.save()
        return user
