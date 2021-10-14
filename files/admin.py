from django.contrib import admin

from .models import AccessUser, File, Comment



admin.site.register(File)



admin.site.register(AccessUser)


admin.site.register(Comment)

# class FileAdmin