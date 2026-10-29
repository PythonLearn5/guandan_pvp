#encoding: utf8
from flask_admin.contrib.mongoengine.filters import BaseMongoEngineFilter
from game.models import Game
from flask_admin.babel import lazy_gettext

class FilterGame(BaseMongoEngineFilter):
    def apply(self, query, value):
        return query.filter(game__exact=Game.objects(name__exact=value).first().id)

    def operation(self):
        return lazy_gettext('exact')

    def get_options(self, view):
        # 应用启动（构建视图缓存）时即会调用本方法；
        # MongoDB 不可达时返回空列表，避免整个应用无法启动
        try:
            return [(obj.name, obj.name) for obj in Game.objects()]
        except Exception:
            return []