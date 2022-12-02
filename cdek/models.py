from django.db import models

from core.models import Point

class CdekPoint(Point):
    code = models.CharField(max_length=10)
    active_status = models.CharField(max_length=10)
    region_name = models.CharField(max_length=100)
    city_code = models.CharField(max_length=20)
    city_name = models.CharField(max_length=20)
    work_time = models.CharField(max_length=300)
    address = models.CharField(max_length=300)
    full_address = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=13)
    note = models.CharField(null=True, blank=True, max_length=1000)


