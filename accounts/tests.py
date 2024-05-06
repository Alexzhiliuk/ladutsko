from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse


class ApplicationViewTests(APITestCase):
    def test_create_application(self):
        url = reverse('application-view')
        data = {
            "email": "a@a.ru",
            "first_name": "name",
            "last_name": "surname",
            "middle_name": "",
            "group_number": "123"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Заявка отправлена!"})

    def test_get_application_form(self):
        url = reverse('application-view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.data)


class ProfileViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.login(username='testuser', password='password')

    def test_update_profile(self):
        url = reverse('profile-view')
        data = {'your_profile_data': 'here'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Профиль успешно изменен!"})

    def test_get_profile_form(self):
        url = reverse('profile-view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_form', response.data)
        self.assertIn('profile_form', response.data)
