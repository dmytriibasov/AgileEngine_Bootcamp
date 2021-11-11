from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


# Create your tests here.
class UsersTests(APITestCase):

    def test_signup(self):
        url = reverse('signup')
        data = {
            'email': 'testinguser@mail.com',
            'password': 'TestUser777',
            'password2': 'TestUser777',
        }
        response = self.client.pos(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
