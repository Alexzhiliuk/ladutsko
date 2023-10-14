from django import forms
from accounts.forms import ProfileEditForm
from .models import Group, Subject, Lesson
from django.contrib.auth.models import User


class AdminProfileEditForm(ProfileEditForm):

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
        fields = ("name", )
        labels = {"name": "Название"}

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'

        self.fields['owner'] = forms.ModelChoiceField(
            queryset=User.objects.filter(profile__type=2).all(),
            label='Владелец',
        )
        self.fields['owner'].required = False


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ("name", "group")
        labels = {"name": "Название", "group": "Группа"}

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ("name", "subject", "test", "video", "photos")
        labels = {"name": "Название", "subject": "Предмет", "test": "Тест", "video": "Видео", "photos": "Фото"}

    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'