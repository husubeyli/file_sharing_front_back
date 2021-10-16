from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.fields import IPAddressField


User = get_user_model()




class UserInfo(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users_info', blank=True, null=True)

    # informations
    browser_family = models.CharField(max_length=255, blank=True, null=True)
    user_id = models.IntegerField()
    username = models.CharField(max_length=188)
    browser_version = models.CharField(max_length=50, blank=True, null=True)
    os_family = models.CharField(max_length=255, blank=True, null=True)
    os_version = models.CharField(max_length=50, blank=True, null=True)
    ip_adress = models.CharField(max_length=255, blank=True, null=True)

    # moderations
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # app_label = 'accounts'
        # managed = False
        verbose_name = 'UserInfo'
        verbose_name_plural = 'UserInfos'



