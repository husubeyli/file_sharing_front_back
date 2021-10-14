from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import AccessUser


class IsUserShowAndWrite(BasePermission):

    # retrieve olanlar ucundu
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user or AccessUser.objects.filter(files=obj, views_user=request.user, access_type__in=[2, 3]).exists():
            return True
        else:
            return False

