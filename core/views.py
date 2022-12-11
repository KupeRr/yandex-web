from rest_framework import generics, status
from rest_framework.response import Response
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404

from core.serializers import UserRequestSerializer
from core.models import UserRequest

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm


class CreateUserRequestView(generics.CreateAPIView):
    serializer_class = UserRequestSerializer

    def create(self, request, *args, **kwargs):
        with atomic():
            user_request = UserRequest()
            user_request.user_id = request.POST.get('user_id')
            user_request.city_region = request.POST.get('city_region')
            user_request.save()

        print(user_request)
        return Response(user_request.id, status=status.HTTP_201_CREATED)

class GetUserRequestView(generics.RetrieveAPIView):
    serializer_class = UserRequestSerializer
    def get(self, request, *args, **kwargs):
        user_request = get_object_or_404(UserRequest, **kwargs)
        return Response(self.get_serializer(user_request).data)

class CleanView(generics.DestroyAPIView):
    def delete(self, request, *args, **kwargs):
        from cdek.models import CdekPoint
        from core.models import Coordinat

        #CdekPoint.objects.all().delete()
        #Coordinat.objects.all().delete()

        return Response(
            len(CdekPoint.objects.all()) + \
            len(Coordinat.objects.all())
        ) 

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "core/register.html"

class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = "core/login.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Авторизация")
        return dict(list(context.items()) + list(c_def.items()))

@csrf_exempt
def login(request):
    return render(request, "core/login.html")

@csrf_exempt
def register(request):
    return render(request, "core/register.html")

@csrf_exempt
def cabinet(request):
    return render(request, "core/cabinet.html")

@csrf_exempt
def download(request):
    return render(request, "core/download.html")