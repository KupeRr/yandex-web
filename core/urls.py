from django.urls import path

from core.views import CreateUserRequestView, GetUserRequestView, CleanView, login, register, cabinet, download, SignUp

app_name = 'core'
urlpatterns = [
    path('login/', login, name='login'),
    path('register/', SignUp.as_view(), name='register'),
    path('cabinet/', cabinet, name='cabinet'),
    path('download/', download, name='download'),
    path('create_user_request/', CreateUserRequestView.as_view()),
    path('get_user_request/<int:pk>/', GetUserRequestView.as_view()),
    path('clean/', CleanView.as_view(), name='test'),
]