
# _meta.model_name
from book import models
# from django.db import models


class DbRouter:
    def db_for_read(self, model, **hints):
        if model._meta.model_name == 'inquiry' or model._meta.model_name == "Inquiry":
            return 'db_inquiry'
        else:
            return 'default'
        return None
 
    def db_for_write(self, model, **hints):
        if model._meta.model_name == 'inquiry' or model._meta.model_name == "Inquiry":
            return 'db_inquiry'
        else:
            return 'default'
        return None
 
    def allow_relation(self, obj1, obj2, **hints):
        return True
 
    def allow_migrate(self, db, app_label, model=None, **hints):
        # if model._meta.model_name == 'inquiry' or model._meta.model_name == "Inquiry":
        #     # model = None
        #     return db == 'db_inquiry'
        # else:
        #     return db == 'default'
        return None



