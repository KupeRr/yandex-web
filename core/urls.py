from django.urls import re_path

from core.views import CreateUserRequestView

app_name = 'core'

urlpatterns = [
    re_path('^create_user_request/', CreateUserRequestView.as_view()),
]