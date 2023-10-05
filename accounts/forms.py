from django import forms
from django.contrib.auth.models import User
from .models import Application


class LoginForm(forms.Form):
    username = forms.CharField(label="Логин")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ("first_name", "last_name", "middle_name", "group_id")
        labels = {"first_name": "Имя", "last_name": "Фамилия", "middle_name": "Отчество", "group_id": "Группа"}

    def __init__(self, *args, **kwargs):
        super(ApplicationForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'
