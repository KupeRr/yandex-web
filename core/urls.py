from django.urls import path

from core.views import CreateUserRequestView, GetUserRequestView, CleanView, login

app_name = 'core'

urlpatterns = [
    path('', login),
    path('create_user_request/', CreateUserRequestView.as_view()),
    path('get_user_request/<int:pk>/', GetUserRequestView.as_view()),
    path('clean/', CleanView.as_view()),
]