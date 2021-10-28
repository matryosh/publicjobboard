from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from .models import JobSeekerModel, CompanyModel, SkillModel, JobExperienceModel, JobListingModel, JobApplicationModel
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from rest_auth.serializers import LoginSerializer as RestAuthLoginSerializer


class UserSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError('Passwords must match.')
        return data

    def create(self, validated_data):

        data = {
            key: value for key, value in validated_data.items()
            if key not in ('password1', 'password2')
        }
        data['password'] = validated_data['password1']
        user = self.Meta.model.objects.create_user(**data)
        user.save()
        if user.user_type == 'JB':
            jobseeker_data = {
                'first_name': '',
                'last_name': '',
                'user': user,
                'jobseeker_id': user.user_number,
            }
            JobSeekerModel.objects.create(**jobseeker_data)
        else:
            company_data = {
                'company_name': '',
                'description': '',
                'user': user,
                'company_id': user.user_number,
            }
            CompanyModel.objects.create(**company_data)
        return user

    class Meta:
        model = get_user_model()
        fields = [
            'email',
            'password1',
            'password2',
            'phone_number',
            'user_type',
            # 'photo',
        ]
        #read_only_fields = ('user_id',)


class LoginSerializer(RestAuthLoginSerializer):
    username = None


class JobSeekerSerializer(serializers.ModelSerializer):\

    skills = serializers.StringRelatedField(many=False)
    job_experience = serializers.StringRelatedField(many=False)

    class Meta:
        model = JobSeekerModel

        fields = [
            'first_name',
            'last_name',
            'skills',
            'job_experience'
        ]

        def create(self, validated_data):
            # create jobseeker model and add SkillsGroupModel to it also
            data = {
                key: value in validated_data.items()
            }
            jobseeker = JobSeekerModel.objects.create(**data)
            print("Model is saved")
            jobseeker.save()
            return jobseeker


class CreateSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkillModel

        fields = [
            'skill',
            'years',
        ]

    def create(self, validated_data):
        data = {
            key: value for key, value in validated_data.items()
        }
        skill = SkillModel.objects.create(**data)
        skill.save()
        return skill



class JobExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobExperienceModel
        fields = [
            'position',
            'company',
            'start_date',
            'end_date',
        ]


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyModel
        fields = [
            'company_name',
            'description',
        ]


class JobListingCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListingModel
        fields = [
            'title',
            'qualifications',
            'responsibilities',
        ]

    def save(self, **kwargs):
        return super().save(**kwargs)

class JobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListingModel
        fields = [
            'title',
            'job_overview',
            'qualifications',
            'responsibilities',
        ]
        read_only_fields =  (
            'applicants'
        )

class CompanyJobsListSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListingModel
        fields = [
            'title',
        ]


class CompanyJoblistingSerializer(serializers.ModelSerializer):
    applicants = serializers.StringRelatedField()
    class Meta:
        model = JobListingModel
        fields = [
            'company',
            'title',
            'job_overview',
            'qualifications',
            'responsibilities',
            'applicants'
        ]

        read_only_fields = (
            'applicants',
        )

class ApplicantJobListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobListingModel
        fields = [
            'company',
            'title',
            'job_overview',
            'qualifications',
            'responsibilities',
            'applicants'
        ]
        read_only_fields = (
            'company',
            'title',
            'job_overview',
            'qualifications',
            'responsibilities',)

class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplicationModel
        fields = [
            'cover_letter',
        ]