from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    number = models.CharField(max_length=32)
    students = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = "Группа"
        verbose_name_plural = "Группы"

    def __str__(self):
        return self.number


class Subject(models.Model):

    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Дисциплина"
        verbose_name_plural = "Дисциплины"

    def __str__(self):
        return self.name


class TeacherGroupSubject(models.Model):
    teacher = models.ForeignKey(User, related_name="subjects", on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject, related_name="items", on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name="subjects", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Дисциплина группы"
        verbose_name_plural = "Дисциплины групп"

    def __str__(self):
        return f"{self.subject.name}, группа {self.group.number}, преподаватель {self.teacher}"

    @property
    def name_for_student(self):
        return f"{self.subject} ({self.teacher})"


class Test(models.Model):
    name = models.CharField(max_length=128)

    class Meta:
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self):
        return self.name

    @property
    def can_be_control(self):
        for question in self.questions.all():
            if question.type == "CH":
                return False
        return True

    def get_question_score(self):
        return 100 / self.questions.count()

    def calculate_score(self, data, user):
        need_check = False  # нужна ли проверка от преподавателя
        question_score = self.get_question_score()  # максимальный балл за вопрос
        try_score = 0  # итоговый балл
        for question in self.questions.all():
            if question.type == "CH":
                answers = {}
                for answer in question.answers.all():
                    answers[answer.pk] = answer.correct
                correct_choices = 0  # количетсво совпадений
                for ans_pk, is_correct in answers.items():
                    if is_correct and data.get(str(ans_pk)) or not is_correct and not data.get(str(ans_pk)):
                        correct_choices += 1
                try_score += question_score * (correct_choices / len(answers))
            elif question.type == "TX":
                student_answer = data.get(str(question.answers.first().pk))
                StudentAnswer.objects.create(user=user, question=question, answer=student_answer)
                need_check = True

        return try_score, need_check


class Question(models.Model):

    class Type(models.TextChoices):
        TEXT = "TX", "Текстовый"
        CHOOSE = "CH", "С вариантами ответа"

    test = models.ForeignKey(Test, related_name="questions", on_delete=models.CASCADE)
    type = models.CharField("Тип", max_length=32, choices=Type.choices)
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

    class Type(models.TextChoices):
        LECTURE = "LC", "Лекция"
        PRACTICAL = "PR", "Практическое занятия"
        LABORATORY = "LR", "Лабораторное занятие"
        CONTROL = "CW", "Контрольная работа"

    type = models.CharField("Тип", max_length=32, choices=Type.choices)
    subject = models.ForeignKey(TeacherGroupSubject, related_name="lessons", on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=128)
    test = models.OneToOneField(Test, on_delete=models.SET_NULL, null=True, blank=True)
    text = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "Занятие"
        verbose_name_plural = "Занятия"

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"

    def get_test_best_try(self):
        tries = [try_.score for try_ in Try.objects.filter(test=self.test)]
        if tries:
            return max(tries)
        return 0

    def get_test_user_best_try(self, user):
        tries = [try_.score for try_ in Try.objects.filter(test=self.test, user=user)]
        if tries:
            return max(tries)
        return 0


class LessonPhoto(models.Model):
    photo = models.ImageField(upload_to="lessons/photos/")
    lesson = models.ForeignKey(Lesson, related_name="photos", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Фото"
        verbose_name_plural = "Фото"

    def __str__(self):
        return f"Фото для {self.lesson.name}"


class LessonVideo(models.Model):
    video = models.FileField(upload_to="lessons/videos/")
    lesson = models.ForeignKey(Lesson, related_name="videos", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Видео"
        verbose_name_plural = "Видео"

    def __str__(self):
        return f"Видео для {self.lesson.name}"


class LessonFile(models.Model):
    file = models.FileField(upload_to="lessons/files/")
    lesson = models.ForeignKey(Lesson, related_name="files", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Файл"
        verbose_name_plural = "Файлы"

    def __str__(self):
        return f"Файл для {self.lesson.name}"


class Try(models.Model):
    user = models.ForeignKey(User, related_name="tests_tries", on_delete=models.CASCADE)
    test = models.ForeignKey(Test, related_name="users_tries", on_delete=models.CASCADE)
    score = models.FloatField()
    need_check = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"

    def __str__(self):
        return f"[{self.score}]{self.user} ({self.test})"

    def checking(self, data):
        question_score = self.test.get_question_score()  # максимальеый балл за вопрос
        checking_score = 0  # баллы за проверку

        for answer in self.students_answers.all():
            checking_score += int(data.get(str(answer.pk), 0))

        self.score += question_score * (checking_score / 10)
        self.need_check = False
        self.save()


class StudentAnswer(models.Model):
    answer = models.CharField(max_length=512)
    question = models.ForeignKey(Question, related_name="students_answers", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="test_answers", on_delete=models.CASCADE)
    student_try = models.ForeignKey(Try, related_name="students_answers", on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = "Ответ студента"
        verbose_name_plural = "Ответы студентов"

    def __str__(self):
        return f"{self.answer[:10]}... ({self.question.test})"