from django.urls import re_path

from cdek.views import AllPointsView

app_name = 'cdek'

urlpatterns = [
    re_path('^cdek_points/<str:city_name>', AllPointsView.as_view()),
]