from django import forms
from accounts.forms import ProfileEditForm
from .models import Group, Subject, TeacherGroupSubject, Lesson, Test, Question, Answer, LessonPhoto, \
    StudentIndividualWork
from django.contrib.auth.models import User


class StudentForm(ProfileEditForm):

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'

        self.fields['group'] = forms.ModelChoiceField(
            queryset=Group.objects.all(),
            label='Группа',
        )
        self.fields['group'].required = False


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("number", )
        labels = {"number": "Номер группы"}

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ("name", )
        labels = {"name": "Название"}

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class TeacherGroupSubjectForm(forms.ModelForm):
    class Meta:
        model = TeacherGroupSubject
        fields = ("teacher", "subject")
        labels = {"teacher": "Преподаватель", "subject": "Дисциплина"}

    def __init__(self, *args, **kwargs):
        super(TeacherGroupSubjectForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class GroupForTeacherSubjectForm(forms.ModelForm):
    class Meta:
        model = TeacherGroupSubject
        fields = ("group", )
        labels = {"group": "Группа"}

    def __init__(self, *args, **kwargs):
        super(GroupForTeacherSubjectForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class LessonForm(forms.ModelForm):

    photos = forms.ImageField(label="Фото", required=False)
    videos = forms.FileField(label="Видео", required=False)
    files = forms.FileField(label="Файлы", required=False)

    class Meta:
        model = Lesson
        fields = ("name", "type", "subject", "test", "text")
        labels = {"name": "Название", "type": "Тип занятия", "subject": "Дисциплина", "test": "Тест", "text": "Текст"}

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'

        self.fields["text"].widget.attrs['class'] = 'form__input full-w'
        self.fields["photos"].widget.attrs['multiple'] = True
        self.fields["videos"].widget.attrs['multiple'] = True
        self.fields["files"].widget.attrs['multiple'] = True


class TestForm(forms.ModelForm):
    class Meta:
        model = Test
        fields = ["name"]
        labels = {"name": "Название"}

    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ("text", "type")
        labels = {"text": "Вопрос", "type": "Тип"}
        widgets = {"type": forms.RadioSelect}

    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ("text", "correct")
        labels = {"text": "Ответ", "correct": ""}

    def __init__(self, *args, **kwargs):
        super(AnswerForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class ExcelForm(forms.Form):
    excel = forms.FileField(label="Excel файл")

    def __init__(self, *args, **kwargs):
        super(ExcelForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class StudentWorkForm(forms.ModelForm):

    class Meta:
        model = StudentIndividualWork
        fields = ("file", )
        labels = {"file": "Файл"}

    def __init__(self, *args, **kwargs):
        super(StudentWorkForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'
