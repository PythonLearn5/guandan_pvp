#encoding: utf8

from flask_admin.contrib.mongoengine import ModelView

class GameAdmin(ModelView):
    page_size = 15
    column_labels = {
            'name': u'赛事名称',
    }
