from django.urls import path

from cdek.views import AllPointsView

app_name = 'cdek'

urlpatterns = [
    path('cdek_points/<int:pk>/', AllPointsView.as_view()),
]