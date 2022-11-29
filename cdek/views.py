import requests

from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from core.models import UserRequest
from cdek.utils import get_city_code
from cdek.models import CdekPoint

class AllPointsView(generics.GenericAPIView):
    queryset = CdekPoint.objects.all()

    def get(self, request, *args, **kwargs):
        user_request = get_object_or_404(UserRequest, **kwargs)
        print('request', user_request)

        city = user_request.city_region.split('-')[0]
        region = user_request.city_region.split('-')[1]
        
        city_code = get_city_code(city, region)
        print('code', city_code)

        one_point = requests.request('GET', f'http://integration.cdek.ru/pvzlist/v1/json?cityid={city_code}').json()['pvz']

        return Response(one_point)
