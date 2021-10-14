from rest_framework import serializers

from .models import AccessUser, File, Comment
from accounts.serializers import UserSerializer


class FileCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = [
            'id',
            'title',
            'description',
            'file',
            'slug',
        ]

    def get_access_type(self, obj):
        return obj.get_access_type_display()

    def validate(self, attrs):
        request = self.context.get('request')
        attrs['user'] = request.user
        return attrs


class FileAcessSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.username')


    class Meta:
        model = File
        fields = [
            'id',
            'user',
            'title',
            'description',
            'file',
            'slug',
        ]


class AcessTypeSerializer(serializers.ModelSerializer):
    access_type = serializers.SerializerMethodField()
    files = FileAcessSerializer(many=True)
    class Meta:
        model = AccessUser
        fields = [
            'id',
            'files',
            'access_type'
        ]

    def get_access_type(self, obj):
        return obj.get_access_type_display()


class FileSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='user.username')
    file_access = AcessTypeSerializer(many=True)

    class Meta:
        model = File
        fields = [
            'id',
            'user',
            'title',
            'description',
            'file_access',
            'file',
            'slug',
        ]


class CommentSerializer(serializers.ModelSerializer):
    users = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Comment
        fields = ['id', 'files', 'users', 'content', ]

    def get_users(self, obj):
        return obj.user.username


class AcessUserFileRetrieveSerializer(serializers.ModelSerializer):
    views_user = UserSerializer(many=True, read_only=True)
    access_type = serializers.SerializerMethodField()

    class Meta:
        model = AccessUser
        fields = [
            'id',
            'views_user',
            'access_type'
        ]

    def get_access_type(self, obj):
        return obj.get_access_type_display()


class FileRetrieveSerialze(serializers.ModelSerializer):
    user = serializers.StringRelatedField(source='username')
    comments = CommentSerializer(many=True, read_only=True)
    file_access = AcessUserFileRetrieveSerializer(many=True)

    class Meta:
        model = File
        fields = [
            'id',
            'user',
            'title',
            'description',
            'file_access',
            'file',
            'comments',
            'slug',
        ]


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'files']

    def validate(self, attrs):
        request = self.context.get('request')
        user = request.user
        file = self.get_fields()
        attrs['users'] = user
        print('yaxwiliq')
        return attrs

    # def create(self, validated_data):
    #     file_id= validated_data.get('files').id
    #     # files =
    #     return super().create(validated_data)
