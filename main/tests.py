from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND)

# Create your tests here.


class TwitTestCase(APITestCase):

    def setUp(self):
        self.email = '123456789@test.com'
        self.password = 'Vvalue2'

    def test_CreateTwit(self):

        user_data = {
            "email": self.email,
            "password": self.password,
            "nickname": "haha"
        }

        self.url = reverse('register')
        response = self.client.post(self.url, user_data, format='json')
        self.assertEqual(HTTP_201_CREATED, response.status_code)

        self.url = reverse('login')
        response = self.client.post(self.url, user_data, format='json')
        self.assertEqual(HTTP_200_OK, response.status_code)
        token = response.content.decode('utf-8').replace('"', '')

        self.client.credentials(HTTP_AUTHORIZATION='Token '+token)
        self.url = reverse('createtwit')
        response = self.client.post(
            self.url, {'content': 'This is a twit'}, format='json')
        self.assertEqual(HTTP_201_CREATED, response.status_code)
