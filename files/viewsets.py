from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .serializers import *
from .models import Comment


class CommentViewsets(ModelViewSet):
    # permission_classes = [IsAuthenticated,]
    queryset = Comment.objects.all()
    permission_classes_by_action = { 
        'create': [IsAuthenticated], 
        'list': [AllowAny],
        'create': [IsAuthenticated], 

    }

    serializers = {
        'list': CommentSerializer,
        'retrieve': CommentSerializer,
        'default': CommentCreateSerializer,
        'create': CommentCreateSerializer,
    }
    # lookup_field = "slug"

    def get_serializer_class(self):
        return self.serializers.get(self.action, self.serializers.get('default'))

    def create(self, request, *args, **kwargs):
        file_id = int(request.data.get('files'))
        user = request.user
        access_user = AccessUser.objects.filter(files__id__in=[file_id], views_user=user, access_type=3)
        if access_user.exists():
            return super(CommentViewsets, self).create(request, *args, **kwargs)
        return Response({ 'message': 'User not access for comment', 'status': status.HTTP_403_FORBIDDEN })

    def list(self, request):
        print(request.data, 'makaka')
        results = CommentSerializer(Comment.objects.all(), many=True)
        return Response(results.data)

    def get_permissions(self):
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]

