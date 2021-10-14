from django.shortcuts import redirect
from django.http import HttpResponse
from files.models import AccessUser, File, User



def check_user_access(view_func):
    def wrapper_func(request,*args,**kwargs):
        # test url : http://127.0.0.1:8000/files/comment/27/?q=4
        id = kwargs['id']
        user_id = int(request.GET.get('q'))
        user = User.objects.get(id=user_id)
        file = File.objects.get(id=id)
        access_qs = AccessUser.objects.filter(files__in=[file],views_user__in=[user], access_type__in=[1,2])
        if user == file.user or access_qs.exists():
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponse('You have no access to show this file')
    return wrapper_func