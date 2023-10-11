from django import forms
from accounts.forms import ProfileEditForm
from .models import Group


class AdminProfileEditForm(ProfileEditForm):

    def __init__(self, *args, **kwargs):
        super(ProfileEditForm, self).__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form__input'

        self.fields['group'] = forms.ModelChoiceField(
            queryset=Group.objects.all(),
            label='Группа',
        )

