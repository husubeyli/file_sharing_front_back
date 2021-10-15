class CheckerRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'accounts':
            return 'users_db'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'accounts':
            return 'users_db'
        return 'default'

    def allow_realtion(self, obj1, obj2, **hint):
        if(obj1._meta.app_label =='accounts' or obj2._meta.app_label == 'accounts'):
            return True
        elif 'accounts' not in [obj1._meta.app_label, obj2._meta.app_label]:
            return True
        return False

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'accounts':
            return db == 'users_db'
        return None


# second users_db database commandos
# ./manage.py migrate --database=users_db
# ./manage.py createsuperuser --database=users_db
