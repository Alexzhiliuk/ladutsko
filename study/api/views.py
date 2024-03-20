from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from study.api.custom_permissions import NotStudent

from study.models import *
from study.forms import SubjectForm, TestForm, QuestionForm
from study.api.serializers import *


class SubjectCreateView(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
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

    authentication_classes = [SessionAuthentication, TokenAuthentication]
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


class TestCreateView(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    def put(self, request, format=None):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Тест добавлен", "auth_request": request.data})

        return Response({"message": "Неверно введены данные!"})

    def get(self, request, format=None):
        form = TestForm()
        response = {
            "form": form.as_div(),
        }
        return Response(response)


class TestEditView(APIView):

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    def put(self, request, pk, format=None):
        test = get_object_or_404(Test, pk=pk)
        serializer = TestSerializer(instance=test, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Тест изменен!", "auth_request": request.data})

        return Response({"message": "Неверно введены данные!"})

    def get(self, request, pk, format=None):
        test = get_object_or_404(Test, pk=pk)
        form = TestForm(instance=test)
        response = {
            "form": form.as_div(),
        }
        return Response(response)


class TestQuestionCreateView(APIView):
    def put(self, request, pk, format=None):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            new_question = serializer.save(test=get_object_or_404(Test, pk=pk))

            if new_question.type == "TX":
                Answer.objects.create(question=new_question, text="Ответ")

            answer_num = 1
            while True:
                answer = request.data.get(f"answer-{answer_num}")
                if answer:
                    correct = bool(request.data.get(f"answer-{answer_num}-correct"))
                    Answer.objects.create(question=new_question, correct=correct, text=answer)
                    answer_num += 1
                    continue
                break

            return Response({"message": "Вопрос для теста добавлен", "auth_request": request.data})
        return Response({"message": "Неверно введены данные!"})

    def get(self, request, *args, **kwargs):
        form = QuestionForm()
        response = {
            "form": form.as_div(),
            "types": Question.Type.choices
        }
        return Response(response)
