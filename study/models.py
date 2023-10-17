from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    owner = models.ForeignKey(User, related_name="study_groups", on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=128)
    students = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return f"{self.id}: {self.name}"


class Subject(models.Model):
    group = models.ForeignKey(Group, related_name="subjects", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предметы"

    def __str__(self):
        return f"{self.name}: {self.group.name}"


class LessonPhoto(models.Model):
    owner = models.ForeignKey(User, related_name="lesson_photos", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    photo = models.ImageField(upload_to="lessons/photos/")

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self):
        return f"{self.name}: {self.owner}"


class Test(models.Model):
    owner = models.ForeignKey(User, related_name="tests", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return f"{self.name}: {self.owner}"


class Question(models.Model):

    class Type(models.IntegerChoices):
        TEXT = 1
        CHOOSE = 2

    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE)
    type = models.IntegerField(choices=Type.choices)
    text = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return f"{self.text[:20]}... ({self.test})"


class Answer(models.Model):

    question = models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    correct = models.BooleanField(default=False)
    text = models.CharField(max_length=256)

    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def __str__(self):
        return f"{self.text[:20]}... ({self.question.test})"


class Lesson(models.Model):
    subject = models.ForeignKey(Subject, related_name="lessons", on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    video = models.FileField(upload_to="lessons/videos/", null=True, blank=True)
    photos = models.ManyToManyField(LessonPhoto, blank=True)
    test = models.ForeignKey(Test, related_name="lessons", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"

    def __str__(self):
        return f"{self.name} ({self.subject})"


class Try(models.Model):
    user = models.ForeignKey(User, related_name="tests_tries", on_delete=models.CASCADE)
    test = models.ForeignKey(Test, related_name="users_tries", on_delete=models.CASCADE)
    score = models.FloatField()

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"

    def __str__(self):
        return f"[{self.score}]{self.user} ({self.test})"
