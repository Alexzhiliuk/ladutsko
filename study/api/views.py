from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.conf import settings

from rest_framework import generics, viewsets, mixins, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from accounts.forms import UserEditForm, ProfileEditForm, UserCreateForm
from accounts.models import Application
from study.api.custom_permissions import NotStudent, AdminOnly, TeacherOnly

from study.models import *
from study.forms import SubjectForm, TestForm, QuestionForm, StudentForm, GroupForm, TeacherGroupSubjectForm, \
    LessonForm, AnswerForm, GroupForTeacherSubjectForm, StudentWorkForm
from study.api.serializers import *


class IndexView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    menu = {
        "admin": {
            "Пользователи": {
                "Преподаватели": reverse_lazy("teachers"),
                "Студенты": reverse_lazy("students"),
            },
            "Заявки": reverse_lazy("applications"),
            "Группы": reverse_lazy("groups"),
            "Дисциплины": reverse_lazy("subjects"),
            "Занятия": reverse_lazy("lessons"),
            "Контроль знаний": reverse_lazy("tests"),
        },
        "teacher": {
            "Группы": reverse_lazy("my-group"),
            "Дисциплины": reverse_lazy("my-subjects"),
            "Занятия": reverse_lazy("my-lessons"),
            "Контроль знаний": reverse_lazy("tests"),
        }
    }

    def get(self, request, format=None):

        user = request.user
        response = {}

        if user.profile.type == 1:
            response = {"menu": self.menu["admin"]}
        if user.profile.type == 2:
            response = {"menu": self.menu["teacher"]}
        if user.profile.type == 3:
            response = {
                "menu": {subject.name_for_student: reverse_lazy("student-subject", kwargs={"pk": subject.pk}) for
                         subject in user.group_set.first().subjects.all()}
            }

        return Response(response)


class TeachersListView(generics.ListAPIView):
    queryset = User.objects.filter(profile__type=2)
    serializer_class = UserSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]


class TeacherEditView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    # {
    # "first_name": "Иван",
    # "last_name": "Иванов",
    # "email": "malyshev@mail.ru",
    # "middle_name": "Кириллович"
    # }

    def put(self, request, pk, format=None):
        teacher = get_object_or_404(User, pk=pk)
        user_serializer = UserEditSerializer(instance=teacher, data=request.data)
        profile_serializer = ProfileEditSerializer(instance=teacher.profile, data=request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save()
            user.username = user.email
            user.save()

            profile_serializer.save()

            return Response({
                "detail": "Преподаватель успешно изменен!",
                "user": user_serializer.data,
                "profile": profile_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при сохранении данных преподавателя."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(User, pk=pk)
        user_form = UserEditForm(instance=teacher)
        profile_form = ProfileEditForm(instance=teacher.profile)

        return Response({
            "user_form": user_form.as_div(),
            "profile_form": profile_form.as_div(),
            "teacher": teacher.pk,
        }, status=status.HTTP_200_OK)


class TeacherCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    # {
    # "first_name": "test",
    # "last_name": "test",
    # "email": "test@test.ru",
    # "password": "1",
    # "middle_name": "test"
    # }
    def put(self, request, *args, **kwargs):
        user_serializer = UserCreateSerializer(data=request.data)
        profile_serializer = ProfileEditSerializer(data=request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():

            new_user = user_serializer.save(username=user_serializer.validated_data.get("email"))
            new_user_password = user_serializer.validated_data.get("password")
            new_user.set_password(new_user_password)

            profile = new_user.profile
            profile.middle_name = profile_serializer.validated_data.get("middle_name")
            profile.type = 2
            profile.save()

            try:
                send_mail(
                    "Данные для входа",
                    f"Логин - ваша почта: {new_user.email}\nПароль: {new_user_password}",
                    settings.EMAIL_HOST_USER,
                    [new_user.email])
            except Exception as err:
                print(err)

            return Response({
                "detail": "Преподаватель успешно создан!",
                "user": user_serializer.data,
                "profile": profile_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при сохранении данных преподавателя."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user_form = UserCreateForm()
        profile_form = ProfileEditForm()
        return Response({
            "user_form": user_form.as_div(),
            "profile_form": profile_form.as_div(),
        }, status=status.HTTP_200_OK)


class DeleteTeacherView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return User.objects.filter(profile__type=2, id=self.kwargs['pk'])


class StudentsListView(generics.ListAPIView):
    queryset = User.objects.filter(profile__type=3)
    serializer_class = UserSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]


class StudentEditView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    # {
    #     "first_name": "Тимофей",
    #     "last_name": "Михайлов",
    #     "email": "mihailov@mail.ru",
    #     "middle_name": "Демидович",
    #     "group": "1"
    # }

    def put(self, request, pk, format=None):
        student = get_object_or_404(User, pk=pk)
        user_serializer = UserEditSerializer(instance=student, data=request.data)
        profile_serializer = StudentSerializer(instance=student.profile, data=request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():
            user = user_serializer.save()
            user.username = user.email
            user.save()

            group = profile_serializer.validated_data.get("group")
            user_group = user.group_set.first()
            profile_serializer.save()

            if group:
                if not (user in group.students.all()):
                    if user_group:
                        user_group.students.remove(user)
                    group.students.add(user)
            else:
                if user_group:
                    user_group.students.remove(user)

            return Response({"detail": "Пользователь успешно изменен!"}, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при изменении пользователя."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        student = get_object_or_404(User, pk=pk)
        user_form = UserEditForm(instance=student)
        profile_form = StudentForm(instance=student.profile)

        student_group = GroupSerializer(student.group_set.first())
        groups = GroupSerializer(Group.objects.all(), many=True)

        return Response({
            "user_form": user_form.as_div(),
            "profile_form": profile_form.as_div(),
            "student_group": student_group.data,
            "groups": groups.data,
            "student": UserSerializer(student).data,
        })


class StudentCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    # {
    #     "first_name": "test",
    #     "last_name": "test",
    #     "email": "test@test.ru",
    #     "password": "1",
    #     "middle_name": "test",
    #     "group": "1"
    # }

    def put(self, request, *args, **kwargs):
        user_serializer = UserCreateSerializer(data=request.data)
        profile_serializer = StudentSerializer(data=request.data)

        if user_serializer.is_valid() and profile_serializer.is_valid():

            new_user = user_serializer.save(username=user_serializer.validated_data.get("email"))
            new_user_password = user_serializer.validated_data.get("password")
            new_user.set_password(new_user_password)

            profile = new_user.profile
            profile.middle_name = profile_serializer.validated_data.get("middle_name")
            profile.type = 3
            profile.save()

            group = profile_serializer.validated_data.get("group")
            if group:
                group.students.add(new_user)

            try:
                send_mail(
                    "Данные для входа",
                    f"Логин - ваша почта: {new_user.email}\nПароль: {new_user_password}",
                    settings.EMAIL_HOST_USER,
                    [new_user.email])
            except Exception as err:
                print(err)

            return Response({
                "detail": "Студент успешно создан!",
                "user": user_serializer.data,
                "profile": profile_serializer.data
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при сохранении данных преподавателя."},
                        status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        user_form = UserCreateForm()
        profile_form = StudentForm()
        groups = GroupSerializer(Group.objects.all(), many=True)
        return Response({
            "user_form": user_form.as_div(),
            "profile_form": profile_form.as_div(),
            "groups": groups.data
        }, status=status.HTTP_200_OK)


class DeleteStudentView(generics.DestroyAPIView):
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return User.objects.filter(profile__type=3, id=self.kwargs['pk'])


class ApplicationsListView(generics.ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]


class ApplicationView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get(self, request, pk, *args, **kwargs):
        application = get_object_or_404(Application, pk=pk)
        user_form = UserCreateForm(initial={
            "first_name": application.first_name,
            "last_name": application.last_name,
            "email": application.email
        })
        profile_form = StudentForm(initial={
            "middle_name": application.middle_name,
            "group": application.group_number
        })
        groups = Group.objects.all()
        groups_serializer = GroupSerializer(groups, many=True)

        response = {
            "user_form": user_form.as_div(),
            "profile_form": profile_form.as_div(),
            "groups": groups_serializer.data,
            "application": ApplicationSerializer(application).data
        }

        if not (Group.objects.filter(number=application.group_number).first()):
            response["detail"] = "Пользователь указал несуществующую группу!"

        return Response(response)


class DeleteApplicationView(generics.DestroyAPIView):
    serializer_class = ApplicationSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return Application.objects.filter(id=self.kwargs['pk'])


class GroupsListView(generics.ListAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]


class GroupEditView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    # {
    #     "number": "456"
    # }
    def put(self, request, pk, *args, **kwargs):
        group = get_object_or_404(Group, pk=pk)
        serializer = GroupSerializer(instance=group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Группа успешно изменена!"}, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при изменении группы."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        group = get_object_or_404(Group, pk=pk)

        form = GroupForm(instance=group)
        subjects_form = TeacherGroupSubjectForm()

        teachers = User.objects.filter(profile__type=2)
        subjects = Subject.objects.all()

        return Response(
            {
                "form": form.as_div(),
                "subjects_form": subjects_form.as_div(),
                "group": GroupSerializer(group).data,
                "teachers": UserSerializer(teachers, many=True).data,
                "subjects": SubjectSerializer(subjects, many=True).data,
            }
        )


class GroupCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    # {
    #     "number": "456"
    # }
    def put(self, request, *args, **kwargs):
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Группа успешно создана!"}, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при создании группы."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        form = GroupForm()
        return Response({"form": form.as_div()})


class DeleteGroupView(generics.DestroyAPIView):
    serializer_class = GroupSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return Group.objects.filter(id=self.kwargs['pk'])


class ExcludeStudentView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def put(self, request, pk, *args, **kwargs):
        student = get_object_or_404(User, pk=pk)
        group = student.group_set.first()
        group.students.remove(student)
        return Response({"detail": "Студент был исключен"},
                        status=status.HTTP_200_OK)


class TeacherGroupSubjectCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    # {
    #     "teacher": "3",
    #     "subject": "2"
    # }
    def put(self, request, pk, *args, **kwargs):
        group = get_object_or_404(Group, pk=pk)
        serializer = TeacherGroupSubjectSerializer(data=request.data)
        if serializer.is_valid():
            new_subject = serializer.save(group=group)

            return Response({
                "detail": "Группе добавлена новая дисциплина!",
                "subject": serializer.data,
            }, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при сохранении данных."},
                        status=status.HTTP_400_BAD_REQUEST)


class DeleteTeacherGroupSubjectView(generics.DestroyAPIView):
    serializer_class = TeacherGroupSubjectSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return TeacherGroupSubject.objects.filter(id=self.kwargs['pk'])


class GroupStudentsListView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get(self, request, pk, *args, **kwargs):
        group = get_object_or_404(Group, pk=pk)
        students = group.students.all()

        return Response({
            "group": GroupSerializer(group).data,
            "students": UserSerializer(students, many=True).data
        })


class SubjectsListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]


class SubjectEditView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def put(self, request, pk, *args, **kwargs):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(instance=subject, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"detail": "Дисциплина успешно изменена!"}, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при изменении дисциплины."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        subject = get_object_or_404(Subject, pk=pk)
        form = SubjectForm(instance=subject)
        items = subject.items.all()
        return Response(
            {
                "form": form.as_div(),
                "subject": SubjectSerializer(subject).data,
                "items": TeacherGroupSubjectSerializer(items, many=True).data
            }
        )


class SubjectCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    # {
    #     "name": "456"
    # }
    def put(self, request, format=None):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Предмет добавлен", "subject": serializer.data})

        return Response({"message": "Неверно введены данные!"})

    def get(self, request, format=None):
        form = SubjectForm()
        response = {
            "form": form.as_div(),
        }
        return Response(response)


class DeleteSubjectView(generics.DestroyAPIView):
    serializer_class = SubjectSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return Subject.objects.filter(id=self.kwargs['pk'])


class LessonsListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]


from rest_framework.parsers import FileUploadParser


class LessonPhotoAddingView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    parser_classes = (FileUploadParser,)

    def put(self, request, pk, format=None, *args, **kwargs):

        lesson = get_object_or_404(Lesson, pk=pk)

        try:
            photo = request.FILES.get("file")
            new_photo = LessonPhoto.objects.create(photo=photo, lesson=lesson)

            return Response(
                {"detail": "Изображение успешно добавлено!", "photo": LessonPhotoSerializer(new_photo).data},
                status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Произошла ошибка при добавлении изображения"},
                            status=status.HTTP_400_BAD_REQUEST)


class LessonVideoAddingView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    parser_classes = (FileUploadParser,)

    def put(self, request, pk, format=None, *args, **kwargs):

        lesson = get_object_or_404(Lesson, pk=pk)

        try:
            video = request.FILES.get("file")
            new_video = LessonVideo.objects.create(video=video, lesson=lesson)

            return Response(
                {"detail": "Видео успешно добавлено!", "photo": LessonVideoSerializer(new_video).data},
                status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Произошла ошибка при добавлении видео"},
                            status=status.HTTP_400_BAD_REQUEST)


class LessonFileAddingView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    parser_classes = (FileUploadParser,)

    def put(self, request, pk, format=None, *args, **kwargs):

        lesson = get_object_or_404(Lesson, pk=pk)

        try:
            file = request.FILES.get("file")
            new_file = LessonFile.objects.create(file=file, lesson=lesson)

            return Response(
                {"detail": "Файл успешно добавлен!", "photo": LessonFileSerializer(new_file).data},
                status=status.HTTP_200_OK)
        except Exception:
            return Response({"detail": "Произошла ошибка при добавлении файла"},
                            status=status.HTTP_400_BAD_REQUEST)


class LessonEditView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    # {
    #     "type": "PR",
    #     "name": "Lesson 2 edited",
    #     "text": "",
    #     "deadline": "2023-12-17T22:00:00+03:00",
    #     "subject": 2,
    #     "test": 7
    # }
    def put(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(instance=lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"detail": "Занятие успешно изменено!"}, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при изменении занятия."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        form = LessonForm(instance=lesson)
        subjects = TeacherGroupSubject.objects.all()
        tests = Test.objects.filter(lesson__isnull=True)
        types = Lesson.type.field.choices
        photos = lesson.photos.all()
        videos = lesson.videos.all()
        files = lesson.files.all()

        return Response({
            "form": form.as_div(),
            "lesson": LessonSerializer(lesson).data,
            "subjects": TeacherGroupSubjectSerializer(subjects, many=True).data,
            "tests": TestSerializer(tests, many=True).data,
            "types": types,
            "photos": LessonPhotoSerializer(photos, many=True).data,
            "videos": LessonVideoSerializer(videos, many=True).data,
            "files": LessonFileSerializer(files, many=True).data,
        })


class LessonCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    # {
    #     "type": "PR",
    #     "name": "Lesson 2 edited",
    #     "text": "",
    #     "deadline": "2023-12-17T22:00:00+03:00",
    #     "subject": 2,
    #     "test": 7
    # }
    def put(self, request, *args, **kwargs):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"detail": "Занятие успешно создано!", "lesson": serializer.data},
                            status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при создании занятия."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        form = LessonForm()
        subjects = TeacherGroupSubject.objects.all()
        tests = Test.objects.filter(lesson__isnull=True)
        types = Lesson.type.field.choices

        return Response({
            "form": form.as_div(),
            "subjects": TeacherGroupSubjectSerializer(subjects, many=True).data,
            "tests": TestSerializer(tests, many=True).data,
            "types": types
        })


class DeleteLessonView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return Lesson.objects.filter(id=self.kwargs['pk'])


class DeleteLessonPhotoView(generics.DestroyAPIView):
    serializer_class = LessonPhotoSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return LessonPhoto.objects.filter(id=self.kwargs['pk'])


class DeleteLessonVideoView(generics.DestroyAPIView):
    serializer_class = LessonVideoSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return LessonVideo.objects.filter(id=self.kwargs['pk'])


class DeleteLessonFileView(generics.DestroyAPIView):
    serializer_class = LessonFileSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [AdminOnly]

    def get_queryset(self):
        return LessonFile.objects.filter(id=self.kwargs['pk'])


class CheckStudentWork(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    # {
    #     "score": 9
    # }
    def put(self, request, pk, *args, **kwargs):
        work = get_object_or_404(StudentIndividualWork, pk=pk)

        score = request.data.get("score")
        work.score = score
        work.save()

        return Response({
            "detail": f"Работа студента {work.user} проверена",
            "score": score
        }, status=status.HTTP_200_OK)

    def get(self, request, pk, *args, **kwargs):
        work = get_object_or_404(StudentIndividualWork, pk=pk)

        return Response({
            "work": StudentIndividualWorkSerializer(work).data,
        })


class TestsListView(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]


class TestCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    def put(self, request, format=None):
        serializer = TestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Тест добавлен", "test": serializer.data})

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


class DeleteTestView(generics.DestroyAPIView):
    serializer_class = Test
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    def get_queryset(self):
        return Test.objects.filter(id=self.kwargs['pk'])


class CheckTestView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    def put(self, request, *args, **kwargs):
        student_try = get_object_or_404(Try, pk=kwargs["pk"])

        student_try.checking(request.data)

        return Response({"detail": "Тест проверен!"}, status=status.HTTP_200_OK)

    def get(self, request, *args, **kwargs):
        student_try = get_object_or_404(Try, pk=kwargs["pk"])

        return Response({
            "try": TrySerializer(student_try).data
        })


class TestQuestionCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

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


class DeleteQuestionView(generics.DestroyAPIView):
    serializer_class = QuestionSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    def get_queryset(self):
        return Question.objects.filter(id=self.kwargs['pk'])


class TestQuestionEditView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    # {
    #     "type": "CH",
    #     "text": "Q3"
    # }
    def put(self, request, pk, *args, **kwargs):
        question = get_object_or_404(Question, pk=pk)
        serializer = QuestionSerializer(instance=question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"detail": "Вопрос успешно изменен!"},
                            status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при измении вопроса."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        question = get_object_or_404(Question, pk=pk)
        form = QuestionForm(instance=question)
        answer_form = AnswerForm()
        return Response({
            "form": form.as_div(),
            "answer_form": answer_form.as_div(),
            "question": QuestionSerializer(question).data,
        })


class AddAnswerVariantView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    def put(self, request, pk, *args, **kwargs):
        question = get_object_or_404(Question, pk=pk)
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question)

            return Response({"detail": "Вариант ответа успешно добавлен!", "answer": serializer.data},
                            status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при добавлении варианта ответа."}, status=status.HTTP_400_BAD_REQUEST)


class AddCorrectTextAnswerView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    def put(self, request, pk, *args, **kwargs):

        question = get_object_or_404(Question, pk=pk)
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            answer = question.answers.first()
            if answer:
                answer.text = serializer.validated_data.get("text")
                answer.save()
                message = "Правильный ответ изменен"
            else:
                serializer.save(question=question)
                message = "Правильный ответ добавлен"

            return Response({"detail": message, "answer": serializer.data},
                            status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при добавлении ответа."}, status=status.HTTP_400_BAD_REQUEST)


class DeleteAnswerView(generics.DestroyAPIView):
    serializer_class = QuestionSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    def get_queryset(self):
        return Answer.objects.filter(id=self.kwargs['pk'])


class MyGroupListView(generics.ListAPIView):
    serializer_class = GroupSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [TeacherOnly]

    def get_queryset(self):
        return {subject.group for subject in TeacherGroupSubject.objects.filter(teacher=self.request.user)}


class AddSubjectToGroup(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [TeacherOnly]

    def put(self, request, pk, *args, **kwargs):
        subject = get_object_or_404(Subject, pk=pk)
        group = request.user.study_groups.first()

        if not group:
            return Response({"detail": "У вас нет группы"}, status=status.HTTP_400_BAD_REQUEST)

        subject.groups.add(group)
        return Response({"detail": "Дисциплина добавлена"}, status=status.HTTP_200_OK)


class RemoveSubjectFromGroup(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [TeacherOnly]

    def put(self, request, pk, *args, **kwargs):
        subject = get_object_or_404(Subject, pk=pk)
        group = request.user.study_groups.first()

        if not group:
            return Response({"detail": "У вас нет группы"}, status=status.HTTP_200_OK)

        subject.groups.remove(group)
        return Response({"detail": "Дисциплина удалена"}, status=status.HTTP_200_OK)


class StudentGradeView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [NotStudent]

    def get(self, request, *args, **kwargs):
        student = get_object_or_404(User, pk=kwargs.get("pk"))
        grade = student.profile.get_grade()
        new_grade = {key.id: value for key, value in grade.items()}

        return Response(
            {
                "student": UserSerializer(student).data,
                "grade": new_grade
            }
        )


class MySubjectsListView(generics.ListAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [TeacherOnly]


class MySubjectEditView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [TeacherOnly]

    def put(self, request, pk, *args, **kwargs):
        subject = get_object_or_404(Subject, pk=pk)
        serializer = SubjectSerializer(instance=subject, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"detail": "Дисциплина успешно изменена!"}, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при изменении дисциплины."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        subject = get_object_or_404(Subject, pk=pk)
        form = SubjectForm(instance=subject)
        items = subject.items.all()
        group_form = GroupForTeacherSubjectForm()
        groups = Group.objects.all()
        return Response(
            {
                "form": form.as_div(),
                "subject": SubjectSerializer(subject).data,
                "items": TeacherGroupSubjectSerializer(items, many=True).data,
                "group_form": group_form.as_div(),
                "groups": GroupSerializer(groups, many=True).data
            }
        )


class MySubjectCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [TeacherOnly]

    # {
    #     "name": "456"
    # }
    def put(self, request, format=None):
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"message": "Предмет добавлен", "subject": serializer.data})

        return Response({"message": "Неверно введены данные!"})

    def get(self, request, format=None):
        form = SubjectForm()
        response = {
            "form": form.as_div(),
        }
        return Response(response)


class MyLessonsListView(generics.ListAPIView):
    serializer_class = LessonSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [TeacherOnly]

    def get_queryset(self):
        lessons = []
        for subject in TeacherGroupSubject.objects.filter(teacher=self.request.user):
            lessons += list(subject.lessons.all())
        return lessons


class MyLessonEditView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [TeacherOnly]

    # {
    #     "type": "PR",
    #     "name": "Lesson 2 edited",
    #     "text": "",
    #     "deadline": "2023-12-17T22:00:00+03:00",
    #     "subject": 2,
    #     "test": 7
    # }
    def put(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        serializer = LessonSerializer(instance=lesson, data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"detail": "Занятие успешно изменено!"}, status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при изменении занятия."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, pk, *args, **kwargs):
        lesson = get_object_or_404(Lesson, pk=pk)
        form = LessonForm(instance=lesson)
        subjects = TeacherGroupSubject.objects.all()
        tests = Test.objects.filter(lesson__isnull=True)
        types = Lesson.type.field.choices
        photos = lesson.photos.all()
        videos = lesson.videos.all()
        files = lesson.files.all()

        return Response({
            "form": form.as_div(),
            "lesson": LessonSerializer(lesson).data,
            "subjects": TeacherGroupSubjectSerializer(subjects, many=True).data,
            "tests": TestSerializer(tests, many=True).data,
            "types": types,
            "photos": LessonPhotoSerializer(photos, many=True).data,
            "videos": LessonVideoSerializer(videos, many=True).data,
            "files": LessonFileSerializer(files, many=True).data,
        })


class MyLessonCreateView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [TeacherOnly]

    # {
    #     "type": "PR",
    #     "name": "Lesson 2 edited",
    #     "text": "",
    #     "deadline": "2023-12-17T22:00:00+03:00",
    #     "subject": 2,
    #     "test": 7
    # }
    def put(self, request, *args, **kwargs):
        serializer = LessonSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()

            return Response({"detail": "Занятие успешно создано!", "lesson": serializer.data},
                            status=status.HTTP_200_OK)

        return Response({"detail": "Ошибка при создании занятия."}, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        form = LessonForm()
        subjects = TeacherGroupSubject.objects.all()
        tests = Test.objects.filter(lesson__isnull=True)
        types = Lesson.type.field.choices

        return Response({
            "form": form.as_div(),
            "subjects": TeacherGroupSubjectSerializer(subjects, many=True).data,
            "tests": TestSerializer(tests, many=True).data,
            "types": types
        })


class MyTestsListView(generics.ListAPIView):
    queryset = Test.objects.all()
    serializer_class = TestSerializer

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [TeacherOnly]


class StudentSubjectView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request, pk, *args, **kwargs):
        user = self.request.user
        subject = get_object_or_404(TeacherGroupSubject, pk=pk)

        if not user.group_set.first():
            return Response({"detail": "Нет разрешения"}, status=status.HTTP_400_BAD_REQUEST)

        if user.group_set.first() != subject.group:
            return Response({"detail": "Нет разрешения"}, status=status.HTTP_400_BAD_REQUEST)

        lessons = {l_type[1]: [] for l_type in Lesson.type.field.choices}
        for lesson in subject.lessons.all():
            lessons[lesson.get_type_display()].append(LessonSerializer(lesson).data)

        return Response({
            "subject": TeacherGroupSubjectSerializer(subject).data,
            "lessons": lessons,
        })


class StudentLessonView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get(self, request, pk, *args, **kwargs):
        user = self.request.user
        lesson = get_object_or_404(Lesson, pk=pk)

        if not user.group_set.first():
            return Response({"detail": "Нет разрешения"}, status=status.HTTP_400_BAD_REQUEST)
        if user.group_set.first() != lesson.subject.group:
            return Response({"detail": "Нет разрешения"}, status=status.HTTP_400_BAD_REQUEST)

        my_best_try = 0
        if lesson.test:
            my_best_try = lesson.get_test_user_best_try(user)

        work_form, work_score = None, None

        if lesson.type == "IW":
            work_form = StudentWorkForm()
            student_work = StudentIndividualWork.objects.filter(user=user, lesson=lesson).first()
            if student_work:
                work_score = student_work.score or "Проверяется"
            else:
                work_score = None

        return Response({
            "lesson": LessonSerializer(lesson).data,
            "best_try": my_best_try,
            "work_score": work_score,
            "work_form": work_form.as_div() if work_form else None
        })


class StudentIndividualWorkView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    parser_classes = (FileUploadParser,)

    def put(self, request, pk, format=None, *args, **kwargs):
        user = self.request.user
        lesson = get_object_or_404(Lesson, pk=pk)

        if not user.group_set.first():
            return Response({"detail": "Нет разрешения"}, status=status.HTTP_400_BAD_REQUEST)
        if user.group_set.first() != lesson.subject.group:
            return Response({"detail": "Нет разрешения"}, status=status.HTTP_400_BAD_REQUEST)

        if StudentIndividualWork.objects.filter(user=user, lesson=lesson):
            return Response({"detail": "Вы уже отправили работу!"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            file = request.FILES.get("file")
            new_work = StudentIndividualWork.objects.create(file=file, lesson=lesson, user=user)

            return Response(
                {"detail": "Файл успешно добавлен!", "work": StudentWorkSerializer(new_work).data},
                status=status.HTTP_200_OK)

        except Exception:
            return Response({"detail": "Произошла ошибка при добавлении работы"},
                            status=status.HTTP_400_BAD_REQUEST)


class StudentTestView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def put(self, request, pk, *args, **kwargs):
        user = self.request.user
        test = get_object_or_404(Test, pk=pk)

        if not user.group_set.first():
            return Response({"detail": "Нет разрешения"}, status=status.HTTP_400_BAD_REQUEST)

        score, need_check = test.calculate_score(request.POST, user)
        student_try = Try.objects.create(user=user, test=test, score=score, need_check=need_check)
        for student_answer in StudentAnswer.objects.filter(user=user, question__test=test, student_try__isnull=True):
            student_answer.student_try = student_try
            student_answer.save()

        if need_check:
            return Response({"detail": "Ваш тест отправлен на проверку"}, status=status.HTTP_200_OK)

        else:
            return Response({"detail": f"Ваш балл составил {score}"}, status=status.HTTP_200_OK)

    def get(self, request, pk, *args, **kwargs):
        user = self.request.user
        test = get_object_or_404(Test, pk=pk)

        if not user.group_set.first():
            return Response({"detail": "Нет разрешения"}, status=status.HTTP_400_BAD_REQUEST)

        if test.lesson.is_late():
            return Response({"detail": "Возможности сдать тест больше нет!"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "test": TestSerializer(test).data,
        })
