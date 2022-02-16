from dataclasses import fields
from rest_framework import serializers
from snippet.models import Snippet

class SnippetSerializer(serializers.ModelSerializer):
  class Meta:
    model = Snippet
    fields = '__all__'