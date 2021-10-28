import base64
from io import BytesIO
import json
from datetime import datetime, date

from django.contrib.auth.models import User
from django.http import response

from rest_framework import serializers, status
import rest_framework
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from PIL import Image

from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from ..models import JobApplicationModel, JobSeekerModel, CompanyModel, JobListingModel, SkillModel, JobExperienceModel

PASSWORD = 'pAssw0rd!'


def create_photo_file():
    data = BytesIO()
    Image.new('RGB', (100, 100)).save(data, 'PNG')
    data.seek(0)
    return SimpleUploadedFile('photo.png', data.getvalue())


def create_custom_user(email='bigbob@gmail.com', password=PASSWORD):
    user = get_user_model().objects.create_user(email, password)
    user.save()
    return user


def create_jobseeker(first_name='Robert', last_name='Robertson', email='bigrobertson@gmail.com'):
    user = create_custom_user(email)
    user.user_type = 'JB'
    user.save()
    data = {
        'first_name': first_name,
        'last_name': last_name,
        'user': user,
        'jobseeker_id': user.user_number,
    }
    JobSeekerModel.objects.create(**data)

    return JobSeekerModel.objects.get(user=user)


def create_job_listing():
    User = create_custom_user()
    User.user_type = 'CM'
    User.save()
    data = {
        'company_name': 'Dinglebobs',
        'description': 'Established in 2021, we do lots of super neat stuff. Some of it is even legal. Which is pretty neat I guess.',
        'company_id': str(User.user_number),
        'user': User
    }

    CompanyModel.objects.create(**data)
    company = CompanyModel.objects.get(company_name='Dinglebobs')
    job_listing_data = {
        'title': 'Gutter Cleaner',
        'job_overview': """As a global leader in 3D design, engineering, and entertainment software, Autodesk helps people imagine, design, and make a better world. Autodesk accelerates better design through an unparalleled depth of experience and a broad portfolio of software to give customers the power to solve their design, business, and environmental challenges.
                                This is an exciting time to join us on our multi-year journey to disrupt the Design to Manufacture world with Fusion 360 by delivering un-precedented value and converging workflows with cloud-based technology. We are rapidly combining many world leading technologies and teams into the Fusion 360 family.
                                """,
        'qualifications': """Bachelor’s Degree in Computer Science or other engineering discipline 
                                C++ course work and projects
                                Outstanding programming, debugging and problem-solving skills
                                Ability to work well in a team to deliver on team goals
                                Familiar with Design Patterns and strong Object-Oriented programming skills
                                Knowledge of data structures, algorithms, and STL
                                Excellent verbal and written communication skills in English""",
        'responsibilities': """As a Gutter Rat, you will be working on implementing exciting User Interface/client-facing features of the core Fusion 360 product as well as some underlying logic.
                            You will:
                            Design, implement, test and maintain features for Fusion 360 based on stakeholders’ requirements (note that our code base is mostly written in C++)
                            Write technical design documents, participate in design and code reviews, develop estimates for tasks and document code
                            Work with an extended team of software developers, QAs and product designers in the US and other worldwide engineering sites.""",
        'company': company,
    }
    job_listing = JobListingModel.objects.create(**job_listing_data)

    return job_listing


class CustomUserModelTest(APITestCase):

    def test_user_can_sign_up(self):
        photo = create_photo_file()
        url = reverse('users:signup')
        data = {
            'email': 'bigbob@gmail.com',
            'password1': PASSWORD,
            'password2': PASSWORD,
            'phone_number': '8482257033',
            'photo': photo
        }

        response = self.client.post(url, data)
        user = get_user_model().objects.last()

        self.assertEqual(url, '/users/signup/')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['phone_number'], user.phone_number)
        self.assertIsNotNone(user.photo)


class JobSeekerModelTest(APITestCase):

    def test_create_jobseeker_model(self):

        User = create_custom_user()
        data = {
            'first_name': 'Robert',
            'last_name': 'Robertson',
            'user': User,
        }

        JobSeekerModel.objects.create(**data)
        jobseeker = JobSeekerModel.objects.get(first_name='Robert')

        self.assertEqual(data['user'], jobseeker.user)
        self.assertEqual(data['first_name'], jobseeker.first_name)
        self.assertEqual(data['last_name'], jobseeker.last_name)

    def test_jobseeker_can_create_skill(self):
        jobseeker = create_jobseeker()
        user_email = jobseeker.user
        self.client.login(email=user_email, password=PASSWORD)

        url = reverse('users:skills_create')
        data = {
            'skill': 'python',
            'years': 2,
        }

        response = self.client.post(url, data)
        skill = SkillModel.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['skill'], skill.skill)
        self.assertEqual(response.data['years'], skill.years)

    def test_jobseeker_can_add_skill(self):
        jobseeker = create_jobseeker()
        user_email = jobseeker.user
        self.client.login(email=user_email, password=PASSWORD)

        url = reverse('users:skills_create')
        data = {
            'skill': 'python',
            'years': 2,
        }
        
        response = self.client.post(url, data)

        skill = SkillModel.objects.get(jobseeker=jobseeker)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(skill.skill, response.data['skill'])

    def test_jobseeker_can_add_jobexperience(self):
        jobseeker = create_jobseeker()
        user_email = jobseeker.user
        self.client.login(email=user_email, password=PASSWORD)

        url = reverse('users:jobseeker', kwargs={'pk': jobseeker.jobseeker_id})
        job_experience_data = {
            'position': 'intern',
            'company': 'InternTech',
            'start_date': '2018-01-01',
            'end_date': '2020-04-01',
        }

        experience = JobExperienceModel.objects.get_or_create(
            **job_experience_data)

        data = {
            'job_experience': experience
        }

        response = self.client.patch(url, data)
        jobguy = JobSeekerModel.objects.get(
            jobseeker_id=jobseeker.jobseeker_id)

        print(response.data['job_experience'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CompanyModelTest(APITestCase):

    def test_create_company_model(self):
        User = create_custom_user()
        data = {
            'company_name': 'Dinglebobs',
            'description': 'Established in 2021, we do lots of super neat stuff. Some of it is even legal. Which is pretty neat I guess.',
            'user': User,
        }

        CompanyModel.objects.create(**data)
        company = CompanyModel.objects.get(company_name='Dinglebobs')

        self.assertEqual(data['user'], company.user)
        self.assertEqual(data['description'], company.description)
        self.assertEqual(data['company_name'], company.company_name)

    def test_edit_company_model(self):

        User = create_custom_user()
        User.user_type = 'CM'
        User.save()
        self.client.login(email=User.email, password=PASSWORD)
        data = {
            'company_name': '',
            'description': '',
            'user': User,
            'company_id': User.user_number
        }

        CompanyModel.objects.create(**data)
        id = data['company_id']
        url = reverse('users:company', kwargs={'pk': id})
        new_data = {
            'company_name': 'Dinglebobs',
            'description': 'Established in 2021, we do lots of super neat stuff. Some of it is even legal. Which is pretty neat I guess.',
        }

        response = self.client.put(url, new_data)
        company = CompanyModel.objects.get(user=User)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(url, f'/users/company/{User.user_number}/')
        self.assertEqual(
            response.data['company_name'], new_data['company_name'])


class JobListingModelTest(APITestCase):

    def test_company_creates_job_listing(self):
        User = create_custom_user()
        User.user_type = 'CM'
        User.save()
        self.client.login(email=User.email, password=PASSWORD)
        data = {
            'company_name': 'Dinglebobs',
            'description': 'Established in 2021, we do lots of super neat stuff. Some of it is even legal. Which is pretty neat I guess.',
            'company_id': str(User.user_number),
            'user': User
        }

        CompanyModel.objects.create(**data)
        company = CompanyModel.objects.get(company_name='Dinglebobs')
        job_listing_data = {
            'title': 'Gutter Cleaner',
            'job_overview': """As a global leader in 3D design, engineering, and entertainment software, Autodesk helps people imagine, design, and make a better world. Autodesk accelerates better design through an unparalleled depth of experience and a broad portfolio of software to give customers the power to solve their design, business, and environmental challenges.
                                This is an exciting time to join us on our multi-year journey to disrupt the Design to Manufacture world with Fusion 360 by delivering un-precedented value and converging workflows with cloud-based technology. We are rapidly combining many world leading technologies and teams into the Fusion 360 family.
                                """,
            'qualifications': """Bachelor’s Degree in Computer Science or other engineering discipline 
                                C++ course work and projects
                                Outstanding programming, debugging and problem-solving skills
                                Ability to work well in a team to deliver on team goals
                                Familiar with Design Patterns and strong Object-Oriented programming skills
                                Knowledge of data structures, algorithms, and STL
                                Excellent verbal and written communication skills in English""",
            'responsibilities': """As a Gutter Rat, you will be working on implementing exciting User Interface/client-facing features of the core Fusion 360 product as well as some underlying logic.
                            You will:
                            Design, implement, test and maintain features for Fusion 360 based on stakeholders’ requirements (note that our code base is mostly written in C++)
                            Write technical design documents, participate in design and code reviews, develop estimates for tasks and document code
                            Work with an extended team of software developers, QAs and product designers in the US and other worldwide engineering sites.""",
        }

        url = reverse('users:create_job_listing')

        response = self.client.post(url, job_listing_data)
        job_listing = JobListingModel.objects.last()

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], job_listing.title)
        self.assertEqual(job_listing.company, company)

    def test_jobseeker_can_apply_to_job(self):
        job_listing = create_job_listing()
        jobseeker = create_jobseeker()
        user_email = jobseeker.user
        self.client.login(email=user_email, password=PASSWORD)

        url = reverse('users:job_listing', kwargs={'job_id': job_listing.id})
        cover_letter = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        data = {
            'cover_letter': cover_letter
        }

        response = self.client.post(url, data)
        job_application = JobApplicationModel.objects.get(applicant=jobseeker)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(job_application.applicant, jobseeker)
        self.assertEqual(job_application.job, job_listing)
        self.assertEqual(response.data['cover_letter'], job_application.cover_letter)
