from django.db import models
from django.contrib.auth.models import User

class Point(models.Model):
    name = models.CharField(max_length=50)

class Coordinat(models.Model):
    point = models.ForeignKey(Point, on_delete=models.CASCADE)
    x = models.FloatField()
    y = models.FloatField()

    @property
    def yandex_format(self):
        return f'{self.x}, {self.y}'

class UserRequest(models.Model):
    user_id = models.IntegerField()
    # <city_name_1-region_name_1 city_name_2-region_name_2 city_name_3-region_name_3 ...>
    city_region = models.CharField(max_length=1000)


class Profile(models.Model):
    username = models.OneToOneField(User, on_delete=models.CASCADE)
    #phone = models.Cha