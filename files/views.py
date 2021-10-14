from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, UpdateAPIView, get_object_or_404
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permissions import IsUserShowAndWrite

from files.models import AccessUser, File
from .serializers import FileCreateSerializer, FileSerializer
from .tasks import delete_file_after_seven_day
# from .permissions import IsUserShowAndWrite

User = get_user_model()



class FilesCreateAPIVIew(ListCreateAPIView):
    serializer_class = FileSerializer
    queryset = File.objects.filter(status=True)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = File.objects.filter(Q(user=self.request.user) | Q(
            Q(file_access__views_user__in = [self.request.user]) &
            Q(file_access__access_type__in = [1,2])
            )
        )
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FileCreateSerializer
        return super().get_serializer_class()

    def post(self, request, *args, **kwargs):

        serializer = FileCreateSerializer(
            data=request.data, context={'request': request})
        if serializer.is_valid():

            serializer.save()
            queryset = File.objects.filter(
                status=True, user=self.request.user).last()

            # for after seven days delete file
            delete_file_after_seven_day.apply_async(
                args=[queryset.id], eta=queryset.is_status_expired)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class FileShareUpdateAPIView(UpdateAPIView, UpdateModelMixin):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data = request.data
        user = User.objects.filter(
            Q(username=data.get('username')) | Q(email=data.get('email'))).first()
        if user != None:
            acces_users_condition = AccessUser.objects.filter(Q(views_user__id__in=[user.id]) & Q(
                files__id__in=[instance.id]) & Q(access_type=int(data.get('access_type'))))
            if acces_users_condition:
                return Response({"message": "User already access", "status": status.HTTP_409_CONFLICT})
            else:
                acces_users = AccessUser.objects.create()
                acces_users.views_user.add(user.id)
                acces_users.files.add(instance.id)
                acces_users.access_type = int(data.get('access_type'))
                acces_users.save()
                return Response({"message": "User access succesfully", "status": status.HTTP_200_OK})
        else:
            return Response({"message": "User not founded", 'status': status.HTTP_400_BAD_REQUEST})


class FileRetrieveAPIView(RetrieveAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, IsUserShowAndWrite ]
    lookup_field = 'slug'

    # def get_object(self):
    #     print('buradayiq')
    #     file = File.objects.filter(Q(user=self.request.user) | Q(user__accessuser__access_type__in = [2,3]))
    #     return file



    # def get_permissions(self):
    #     print(self.request.method, 'alada')
    #     if self.request.method == 'GET':
    #         return IsAuthenticatedOrReadOnly
    #     return IsAuthenticated



from django.shortcuts import render
from .models import Comment
from .decorators import check_user_access

@check_user_access
def home(request, id):
    user_id = request.GET.get('q')
    context = {}
    file = File.objects.get(id=id)
    user = User.objects.get(id=user_id)
    comments = Comment.objects.filter(files=file)
    context['file'] = file
    context['comments'] = comments
    if user == file.user:
        check_access_for_wite_smth = True
    else:
        check_access_for_wite_smth = AccessUser.objects.filter(
            access_type__in=[2],
            files__in = [file],
            views_user__in = [user]
        ).exists()
    context['check_access_for_wite_smth'] = check_access_for_wite_smth
    return render(request,'home.html',context)