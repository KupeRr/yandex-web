from rest_framework import generics, status
from rest_framework.response import Response
from django.db.transaction import atomic

from core.serializers import UserRequestSerializer
from core.models import UserRequest

class CreateUserRequestView(generics.CreateAPIView):
    serializer_class = UserRequestSerializer

    def create(self, request, *args, **kwargs):
        with atomic():
            user_request = UserRequest()
            user_request.user_id = request.POST.get('user_id')
            user_request.cities = request.POST.get('cities')
            user_request.save()

        return Response(user_request.id, status=status.HTTP_201_CREATED)

