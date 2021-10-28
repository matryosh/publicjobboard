from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings
from django.contrib.auth import get_user_model

from uuid import uuid4
from django.db.models.base import Model

from django.db.models.fields import NullBooleanField
from django.db.models.fields.related import ForeignKey
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password, **fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **fields):
        fields.setdefault('is_staff', True)
        fields.setdefault('is_superuser', True)
        fields.setdefault('is_active', True)

        if fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))
        if fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True'))
        return self.create_user(email, password, **fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = None
    phone_number = PhoneNumberField(blank=True, editable=True)
    user_number = models.UUIDField(
        primary_key=True, default=uuid4, editable=False, unique=True)
    photo = models.ImageField(upload_to='media/photos', null=True, blank=True)
    JOBSEEKER = 'JB'
    COMPANY = 'CM'
    USER_TYPE_CHOICES = [
        (JOBSEEKER, 'Jobseeker'),
        (COMPANY, 'Company'),
    ]
    user_type = models.CharField(
        max_length=2,
        choices=USER_TYPE_CHOICES,
        default=JOBSEEKER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def __str__(self):
        return self.email


# jobseeker models here
class JobExperienceModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    position = models.CharField(max_length=128, blank=False)
    company = models.CharField(max_length=128, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return str(self.id) + ":" + self.position


class JobSeekerModel(models.Model):

    first_name = models.CharField(max_length=128, blank=True)
    last_name = models.CharField(max_length=128, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    user_bio = models.CharField(max_length=1200, blank=True)
    jobseeker_id = models.SlugField(
        max_length=128, primary_key=True, default='')
    job_experience = models.ForeignKey(JobExperienceModel, on_delete=models.CASCADE, default='', null=True, blank=True)
    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class SkillModel(models.Model):
    skill = models.CharField(max_length=64, blank=False)
    years = models.IntegerField()
    jobseeker = ForeignKey(JobSeekerModel, on_delete=models.CASCADE, default='', null=True, blank=True)
    id = models.UUIDField(primary_key=True, default=uuid4,
                          editable=False, max_length=128)

    def __str__(self):
        return self.skill


# Company related models here
class CompanyModel(models.Model):
    company_name = models.CharField(max_length=128, blank=True)
    description = models.CharField(max_length=512, blank=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default='')
    company_id = models.SlugField(max_length=128, primary_key=True, default='')

    def __str__(self):
        return self.company_name


class JobListingModel(models.Model):

    OPEN = 'OP'
    CLOSED = 'CL'

    JOB_TYPE_CHOICES = [
        (OPEN, 'Open'),
        (CLOSED, 'Closed'),
    ]

    user_type = models.CharField(
        max_length=2,
        choices=JOB_TYPE_CHOICES,
        default=OPEN
    )

    title = models.CharField(max_length=128)
    job_overview = models.TextField(max_length=250, blank=True)
    qualifications = models.TextField()
    responsibilities = models.TextField()
    company = models.ForeignKey(CompanyModel, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id) + ": " + self.title


class JobApplicationModel(models.Model):
    
    job = models.ForeignKey(JobListingModel, on_delete=models.CASCADE)
    applicant = models.ForeignKey(JobSeekerModel, on_delete=models.CASCADE)
    id = models.UUIDField(primary_key=True, default=uuid4,
                          editable=False, max_length=128)
    cover_letter = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.job.title}: {self.applicant.user}"