#encoding:utf8

import mongoengine


class MongoEngineShim:
    """替代 flask_mongoengine.MongoEngine 的最小实现。

    flask_mongoengine 1.0.0 依赖已在 Flask 2.3 中移除的 flask.json.JSONEncoder，
    无法在 Flask 3.x 下导入；而本项目只用到模型字段定义与 init_app 建连接，
    这里直接委托给 mongoengine 即可。
    """

    def init_app(self, app):
        settings = dict(app.config.get('MONGODB_SETTINGS') or {})
        db_name = settings.get('db') or 'guandan'
        kwargs = {
            'db': db_name,
            'host': settings.get('host', 'localhost'),
            'port': int(settings.get('port', 27017)),
        }
        username = settings.get('username')
        if username:
            kwargs['username'] = username
            kwargs['password'] = settings.get('password')
            kwargs['authentication_source'] = (
                settings.get('authentication_source')
                or settings.get('authentication_database')
                or db_name
            )
        mongoengine.connect(**kwargs)

    def __getattr__(self, name):
        return getattr(mongoengine, name)


db = MongoEngineShim()
