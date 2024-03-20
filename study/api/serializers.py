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


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['text', 'type']

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