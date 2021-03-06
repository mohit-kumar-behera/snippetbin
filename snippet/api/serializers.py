from rest_framework import serializers
from snippet.models import Snippet
from account.serializers import UserSerializer
from home.serializers import TinyURLSerializer

class SnippetSerializer(serializers.ModelSerializer):
  user = UserSerializer(many = False)
  urls = serializers.SerializerMethodField()
  datetime = serializers.SerializerMethodField()
  has_expired = serializers.SerializerMethodField()

  class Meta:
    model = Snippet
    fields = '__all__'
  
  def get_urls(self, snippet):
    urls = snippet.tinyurl
    serializer = TinyURLSerializer(urls, many = False)
    return serializer.data
  
  def get_datetime(self, snippet):
    result = snippet.extract_delta_datetime()
    return result
  
  def get_has_expired(self, snippet):
    return snippet.if_has_expired()
