from rest_framework import serializers
from accounts.models import *
from django.contrib.auth.models import User


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['email', 'first_name', 'last_name', 'middle_name', 'group_number']


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']


class ProfileEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['middle_name']

{
 "email": "" ,
 "first_name": "",
"last_name": "",
"middle_name": ""
}