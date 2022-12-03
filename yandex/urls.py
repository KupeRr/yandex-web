from django.urls import path

from yandex.views import GetAllPoints

app_name = 'yandex'

urlpatterns = [
    path('convert_points/<int:request_id>/', GetAllPoints.as_view()),
]