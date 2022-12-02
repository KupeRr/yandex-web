from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from core.models import UserRequest
from cdek.utils import update_db
from cdek.models import CdekPoint
from cdek.serializers import CdekPointSerializer

class AllPointsView(generics.RetrieveAPIView):
    queryset = CdekPoint.objects.all()
    serializer_class = CdekPointSerializer

    def get(self, request, *args, **kwargs):
        user_request = get_object_or_404(UserRequest, **kwargs)
        print('request', user_request)

        city = user_request.city_region.split('-')[0]
        region = user_request.city_region.split('-')[1]

        update_db(city, region)

        return Response(len(CdekPoint.objects.all()))
