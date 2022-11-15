from rest_framework import generics
from rest_framework.response import Response

import requests

class AllPointsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        print(kwargs['city_name'])
        one_point = requests.request('GET', 'http://integration.cdek.ru/pvzlist/v1/json?cityid=430').json()['pvz'][0]

        return Response(one_point)
