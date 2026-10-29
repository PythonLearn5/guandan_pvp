#encoding: utf8

from flask_admin.contrib.mongoengine import ModelView
from flask_admin import BaseView, expose
import sys
sys.path.append('..')
from filters import FilterGame

class GameRecordAdmin(ModelView):
    page_size = 15
    column_labels = {
            'game': u'赛事',
            'round': u'轮次',
            'desk_no': u'桌号',
            'red': u'红方',
            'blue': u'蓝方',
            'result': u'赛果',
            'diff': u'级差',
    }

    column_filters = ['round', FilterGame('game', u'赛事')]