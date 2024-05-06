from rest_framework import serializers

from accounts.models import Profile, Application
from study.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")


class UserCreateSerializer(UserEditSerializer):

    password = serializers.CharField(max_length=64)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")


class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("middle_name",)


class ApplicationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Application
        fields = "__all__"


class StudentSerializer(ProfileEditSerializer):

    group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = Profile
        fields = ("middle_name", "group")


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"
        read_only_fields = ["id", "students"]


class TeacherGroupSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherGroupSubject
        fields = ("teacher", "subject")


class GroupForTeacherSubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeacherGroupSubject
        fields = ("group", )


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['id', 'name']
        read_only_fields = ["id"]


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        read_only_fields = ["id"]


class LessonPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonPhoto
        fields = '__all__'
        read_only_fields = ["id"]


class LessonVideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonVideo
        fields = '__all__'
        read_only_fields = ["id"]


class LessonFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = LessonFile
        fields = '__all__'
        read_only_fields = ["id"]


class StudentIndividualWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentIndividualWork
        fields = '__all__'
        read_only_fields = ["id", "user", "lesson", "file"]


class StudentWorkSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentIndividualWork
        fields = ("file", )


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = "__all__"
        read_only_fields = ["id"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = "__all__"
        read_only_fields = ["id", "test"]


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        read_only_fields = ["id", "question"]


class TrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Try
        fields = "__all__"
        read_only_fields = ["id"]
#
# {
#  "name": "" ,
# }

# {
# "text": "Q3",
# "type": "CH",
# "answer-1": "A1",
# "answer-1-correct": 1
# }