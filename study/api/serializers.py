from rest_framework import serializers
from study.models import *


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ['name']


class TestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Test
        fields = ['name']

#
# {
#  "name": "" ,
# }