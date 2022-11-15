from rest_framework import serializers

from cdek.models import CdekPoint

class CdekPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = CdekPoint
        fields = '__all__'