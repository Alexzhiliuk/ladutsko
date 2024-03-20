from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User

from accounts.models import Profile
from .models import Subject, Test


class SubjectCreateViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.login(username='testuser', password='password')

    def test_create_subject(self):
        url = reverse('subject-create-view')
        data = {
            "name": "New subject",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Предмет добавлен"})

    def test_get_subject_form(self):
        url = reverse('subject-create-view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.data)


class SubjectEditViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.login(username='testuser', password='password')
        self.subject = Subject.objects.create(name='Test subject')

    def test_update_subject(self):
        url = reverse('subject-edit-view', args=[self.subject.pk])
        data = {
            "name": "New subject udpated",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Предмет изменен!"})

    def test_get_subject_form(self):
        url = reverse('subject-edit-view', args=[self.subject.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.data)


class TestCreateViewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.login(username='testuser', password='password')

    def test_create_test(self):
        url = reverse('test-create-view')
        data = {
            "name": "New test",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Тест добавлен", "auth_request": data})

    def test_get_test_form(self):
        url = reverse('test-create-view')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.data)


class TestEditViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.login(username='testuser', password='password')
        self.test = Test.objects.create(name='Test test data')

    def test_update_test(self):
        url = reverse('test-edit-view', args=[self.test.pk])
        data = {
            "name": "New test",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Тест изменен!", "auth_request": data})

    def test_get_test_form(self):
        url = reverse('test-edit-view', args=[self.test.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.data)


class TestQuestionCreateViewTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='password')
        self.client.login(username='testuser', password='password')
        self.test = Test.objects.create(name='Test test data')

    def test_create_question(self):
        url = reverse('test-question-create-view', args=[self.test.pk])
        data = {
            "text": "Q3",
            "type": "CH",
            "answer-1": "A1",
            "answer-1-correct": 1
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Вопрос для теста добавлен", "auth_request": data})

    def test_get_question_form(self):
        url = reverse('test-question-create-view', args=[self.test.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('form', response.data)
