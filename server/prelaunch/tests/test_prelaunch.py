import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from prelaunch.models import PrelaunchModel
# Create your tests here.

class PrelaunchTest(APITestCase):

    def test_user_can_enter_email(self):
        response = self.client.post(reverse('prelaunch'), data={
            'email': 'burgerbob@gmail.com'
        })

        prelaunch = PrelaunchModel.objects.last()

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(response.data['email'], prelaunch.email)