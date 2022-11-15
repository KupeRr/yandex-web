from rest_framework import generics
from rest_framework.response import Response

class AllPointsView(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        return Response(200)
