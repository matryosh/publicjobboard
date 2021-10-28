from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from .models import (CompanyModel, CustomUser, JobSeekerModel,
 SkillModel, JobListingModel, JobApplicationModel)
# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(DefaultUserAdmin):
    ordering=('email',)
    list_display = ('email', 'user_number', 'phone_number')
    fieldsets = (
        (None, {
            'fields': ('email',)
            }),
        )


@admin.register(JobSeekerModel)
class JobSeekerAdmin(admin.ModelAdmin):
    ordering=('jobseeker_id',)
    list_display=('jobseeker_id', 'first_name', 'last_name')


@admin.register(CompanyModel)
class CompanyAdmin(admin.ModelAdmin):
    ordering=('company_id', )
    list_display = ('company_id', 'company_name',)

@admin.register(SkillModel)
class SkillAdmin(admin.ModelAdmin):
    pass

@admin.register(JobListingModel)
class JobListingAdmin(admin.ModelAdmin):
    pass

@admin.register(JobApplicationModel)
class JobApplicationAdmin(admin.ModelAdmin):
    pass