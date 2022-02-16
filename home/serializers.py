from rest_framework import serializers
from home.models import TinyURL

class TinyURLSerializer(serializers.ModelSerializer):
  class Meta:
    model = TinyURL
    fields = ('original_url', 'shorten_url')