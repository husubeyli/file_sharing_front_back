from django.urls import path
from .views import FilesCreateAPIVIew, FileShareUpdateAPIView, FileRetrieveAPIView, home
from .routers import router

urlpatterns = [
    path('comment/<id>/',home,name='home'),

    path('create/', FilesCreateAPIVIew.as_view()),
    path('access/<slug:slug>/', FileShareUpdateAPIView.as_view()),
    path('detail/<slug:slug>/', FileRetrieveAPIView.as_view()),
]


urlpatterns += router.urls