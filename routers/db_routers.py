class AuthRouter:
    router_app_labels = {'auth', 'contenttypes', 'session', 'admin'}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.router_app_labels:
            return 'users_db'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.router_app_labels:
            return 'users_db'
        return None

    def allow_realtion(self, obj1, obj2, **hint):
        if(obj1._meta.app_label in self.router_app_labels or obj2._meta.app_label in self.router_app_labels):
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'users_db'
        return None


# second users_db database commandos
# ./manage.py migrate --database=users_db
# ./manage.py createsuperuser --database=users_db
