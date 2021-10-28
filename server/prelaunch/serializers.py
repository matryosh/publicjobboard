from rest_framework import serializers

from .models import PrelaunchModel

class PrelaunchSerializer(serializers.ModelSerializer):
    class Meta:
        model = PrelaunchModel
        fields = ['email',]