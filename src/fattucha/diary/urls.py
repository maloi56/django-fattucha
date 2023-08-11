from datetime import datetime

from django.urls import path, register_converter

from diary.views import (AddInDiaryView, AddProductView, ChangeFoodView,
                         DairyView, ReportView, ReportWeekView, remove_food)

# AddInDiaryView
app_name = 'diary'


class DateConverter:
    regex = '\d{4}-\d{2}-\d{2}'

    def to_python(self, value):
        return datetime.strptime(value, '%Y-%m-%d').date()

    def to_url(self, value):
        return value


register_converter(DateConverter, 'yyyy')

urlpatterns = [
    path('', DairyView.as_view(), name='diary'),
    path('?date=/<yyyy:date>/', DairyView.as_view(), name='diary'),
    path('add_product/', AddProductView.as_view(), name='add_product'),
    path('change_food/<int:pk>', ChangeFoodView.as_view(), name='change_food'),
    # path('add_in_diary/', add_in_diary, name='add_in_diary'),

    path('add_in_diary/', AddInDiaryView.as_view(), name='add_in_diary'),
    path('remove_food/<int:food_id>', remove_food, name='remove_food'),

    path('reports/', ReportView.as_view(), name='reports'),
    # path('reports/?date=/<yyyy:date>/', ReportView.as_view(), name='reports'),
    path('reports/date/<yyyy:date>/', ReportView.as_view(), name='reports'),
    path('reports/period/<int:year>/<int:week>/', ReportWeekView.as_view(), name='week_reports'),

]
