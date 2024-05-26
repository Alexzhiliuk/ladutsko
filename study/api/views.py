from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication
from study.api.custom_permissions import NotStudent

from study.models import *
from study.forms import SubjectForm
from study.api.serializers import *


class SubjectCreateView(APIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [NotStudent]

    def put(self, request, format=None):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Предмет добавлен"})

        return Response({"message": "Неверно введены данные!"})

    def get(self, request, format=None):
        form = SubjectForm()
        response = {
            "form": form.as_div(),
        }
        return Response(response)


class SubjectEditView(APIView):

    authentication_classes = [SessionAuthentication]
    permission_classes = [NotStudent]

    def put(self, request, pk, format=None):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(instance=subject, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Предмет изменен!"})

        return Response({"message": "Неверно введены данные!"})

    def get(self, request, pk, format=None):
        subject = get_object_or_404(Subject, pk=pk)
        form = SubjectForm(instance=subject)
        response = {
            "form": form.as_div(),
        }
        return Response(response)
