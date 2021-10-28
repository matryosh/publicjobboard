from django.urls import path, include
from .views import (JobsListView, SignUpView, JobSeekerView, CompanyView,
 CreateSkillView, CreateJobExperienceView,
  CreateJobListingView, CompanyJobListingView, JobListingView, JobApplicationView)


app_name='users'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('jobseeker/<pk>/', JobSeekerView.as_view(), name='jobseeker'),
    path('company/<pk>/', CompanyView.as_view(), name='company'),
    path('skills/create/', CreateSkillView.as_view(), name='skills_create'),
    path('jobexperience/create', CreateJobExperienceView.as_view(), name='create_jobexperience'),
    path('joblisting/create', CreateJobListingView.as_view(), name='create_job_listing'),
    path('joblist', JobsListView.as_view(), name='jobslist'),
    path('company/<pk>', CompanyJobListingView.as_view(), name="company_job_listing"),
    path('<str:job_id>/apply', JobApplicationView.as_view(), name="job_listing"),
    path('', include('dj_rest_auth.urls')),
]
