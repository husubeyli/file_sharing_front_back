from django.conf import settings

# Routing table defined in setting
from django.contrib import admin

server_site = admin.AdminSite('default')
local_site = admin.AdminSite('users_db')


class AuthRouter(object):
    router_app_labels = {'accounts'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label == "accounts":
            return 'users_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == "accounts":
            return 'users_db'
        return None

    def allow_realtion(self, obj1, obj2, **hint):
        if(obj1._meta.app_label  == "accounts" or obj2._meta.app_label  == "accounts"):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label  == "accounts":
            return db == 'users_db'
        return None


# second users_db database commandos
# ./manage.py migrate --database=users_db
# ./manage.py createsuperuser --database=users_db
