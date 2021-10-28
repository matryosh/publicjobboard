from functools import partial
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.decorators import login_required
from rest_framework import generics, permissions
from rest_framework.decorators import api_view

from .models import (CompanyModel, JobSeekerModel, SkillModel,
 JobExperienceModel, JobListingModel, JobApplicationModel)
from .serializers import (UserSerializer, JobSeekerSerializer, CompanySerializer, CreateSkillSerializer,
 JobExperienceSerializer, JobListingCreationSerializer, CompanyJoblistingSerializer,
  ApplicantJobListingSerializer, CompanyJobsListSerializer, JobApplicationSerializer)
from .permissions import IsCompany, IsProperCompany, IsJobseeker, IsProperJobseeker

# Create your views here.

class SignUpView(generics.CreateAPIView):
    get_query_set=get_user_model().objects.all()
    serializer_class=UserSerializer


class LoginView():
    pass


class JobSeekerView(generics.RetrieveUpdateAPIView):
    queryset = JobSeekerModel.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsProperJobseeker]


class CompanyView(generics.UpdateAPIView):
    queryset = CompanyModel.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsProperCompany]


class CreateSkillView(generics.CreateAPIView):
    queryset = SkillModel.objects.all()
    serializer_class = CreateSkillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        jobseeker = JobSeekerModel.objects.get(user=user)
        serializer.save(jobseeker=jobseeker)
        return super().perform_create(serializer)


class CreateJobExperienceView(generics.CreateAPIView):
    queryset = JobExperienceModel.objects.all()
    serializer_class = JobExperienceSerializer
    permission_classes = [permissions.IsAuthenticated]


class CreateJobListingView(generics.CreateAPIView):
    queryset = JobListingModel.objects.all()
    serializer_class = JobListingCreationSerializer
    permission_classes = [permissions.IsAuthenticated, IsCompany]

    def perform_create(self, serializer):
        user = self.request.user
        company = CompanyModel.objects.get(user=user)
        serializer.save(company=company)
        return super().perform_create(serializer)


class CompanyJobListingView(generics.RetrieveUpdateDestroyAPIView):
    queryset = JobListingModel.objects.all()
    serializer_class = CompanyJoblistingSerializer
    permission_classes = [permissions.IsAuthenticated,]


class JobsListView(generics.ListAPIView):
    queryset = JobListingModel.objects.all()
    serializer_class = CompanyJobsListSerializer
    permission_classes = [permissions.IsAuthenticated]


class JobListingView(generics.RetrieveUpdateAPIView):
    queryset = JobListingModel.objects.all()
    serializer_class = ApplicantJobListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsJobseeker]


class JobApplicationView(generics.CreateAPIView):
    queryset = JobApplicationModel.objects.all()
    serializer_class = JobApplicationSerializer

    def perform_create(self, serializer):
        user = self.request.user
        applicant = JobSeekerModel.objects.get(user=user)
        job = JobListingModel.objects.get(id=self.kwargs.get('job_id'))
        serializer.save(applicant=applicant, job=job)
        return super().perform_create(serializer)