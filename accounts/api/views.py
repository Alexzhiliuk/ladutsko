from sqlite3 import IntegrityError

from rest_framework import generics, viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from accounts.forms import ApplicationForm, UserEditForm, ProfileEditForm
from accounts.models import *
from accounts.api.serializers import *


class ApplicationView(APIView):

	def put(self, request, format=None):
		serializer = ApplicationSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()

			return Response({"message": "Заявка отправлена!"})

		return Response({"message": "Неверно введены данные!"})

	def get(self, request, format=None):
		form = ApplicationForm()
		response = {
			"form": form.as_div(),
		}
		return Response(response)


class ProfileView(APIView):
	authentication_classes = [SessionAuthentication, TokenAuthentication]
	permission_classes = [IsAuthenticated]

	def put(self, request, format=None):
		user = request.user
		user_serializer = UserEditSerializer(instance=user, data=request.data)
		profile_serializer = ProfileEditSerializer(instance=user.profile, data=request.data)
		if user_serializer.is_valid() and profile_serializer.is_valid():
			try:
				user_serializer.save(username=user.email)
			except IntegrityError:
				return Response({"message": "Такой email уже существует!"})

			profile_serializer.save()
			return Response({"message": "Профиль успешно изменен!"})

		return Response({"message": "Форма заполнена некорректно!"})

	def get(self, request, format=None):
		user = request.user
		user_form = UserEditForm(instance=user)
		profile_form = ProfileEditForm(instance=user.profile)
		response = {
			"user_form": user_form.as_div(),
			"profile_form": profile_form.as_div(),
		}
		return Response(response)
