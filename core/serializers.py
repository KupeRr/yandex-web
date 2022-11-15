from rest_framework import serializers

from core.models import UserRequest

class UserRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRequest
        fields = '__all__'