from django.contrib import admin
from .models import User, UserInfo



class MultiDBListFilter(admin.SimpleListFilter):
    title = 'database'
    parameter_name = 'db'

    def lookups(self, request, model_admin):
        return tuple((db, db) for db in ['default'])

    def value(self):
        return super(MultiDBListFilter, self).value() or 'default'

    def queryset(self, request, queryset):
        return queryset

    def choices(self, cl):
        choices = super(MultiDBListFilter, self).choices(cl)
        choices.next()  # Skip `All` choice.
        for choice in choices:
            yield choice




class UserInfoAdmin(admin.ModelAdmin):
    using = 'users_db'

    class Meta:
        unique_together = ('user_id', 'user_name')

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'other' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'other' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'other' database.
        return super(UserInfoAdmin, self).get_queryset(request).using(self.using)
admin.site.register(UserInfo, UserInfoAdmin)