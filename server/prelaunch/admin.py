from django.contrib import admin
from .models import PrelaunchModel
# Register your models here.

@admin.register(PrelaunchModel)
class PrelaunchAdmin(admin.ModelAdmin):
    fields = (
        'email',
    )
    list_display = (
        'email',
    )