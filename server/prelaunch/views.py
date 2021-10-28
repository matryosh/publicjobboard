from django.shortcuts import render
from rest_framework import generics

from .serializers import PrelaunchSerializer
from .models import PrelaunchModel
# Create your views here.

class PrelaunchView(generics.CreateAPIView):
    queryset = PrelaunchModel.objects.all()
    serializer_class = PrelaunchSerializer