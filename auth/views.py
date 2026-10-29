#encoding: utf8

from flask_admin.contrib.mongoengine import ModelView
from flask_security import current_user

class UserAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')

class RoleAdmin(ModelView):
    def is_accessible(self):
        return current_user.has_role('admin')