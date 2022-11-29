from rest_framework import generics, status
from rest_framework.response import Response
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404

from core.serializers import UserRequestSerializer
from core.models import UserRequest

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

