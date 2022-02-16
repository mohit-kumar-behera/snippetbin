from rest_framework import serializers
from snippet.models import Snippet
from account.serializers import UserSerializer
from home.serializers import TinyURLSerializer

from django.utils import timezone
import datetime

class SnippetSerializer(serializers.ModelSerializer):
  user = UserSerializer(many = False)
  urls = serializers.SerializerMethodField()
  datetime = serializers.SerializerMethodField()

  class Meta:
    model = Snippet
    fields = '__all__'
  
  def get_urls(self, snippet):
    urls = snippet.tinyurl
    serializer = TinyURLSerializer(urls, many = False)
    return serializer.data
  
  def get_datetime(self, snippet):
    now = timezone.now()
    created_at = snippet.created_at
    
    if now - datetime.timedelta(hours=24) <= created_at <= now + datetime.timedelta(hours=24):
      """ WITHIN 24 HOURS """
      curr_hour = int(now.strftime('%H'))
      created_at_hour = int(created_at.strftime('%H'))
      diff = curr_hour - created_at_hour
      type = 'hour'
      
      if diff == 0:
        curr_min = int(now.strftime('%M'))
        created_at_min = int(created_at.strftime('%M'))
        diff = curr_min - created_at_min
        type = 'min'

      result = f'{diff} {type} ago' if diff > 0 else 'few sec ago'
    else:
      result = created_at.strftime("%b %d, %Y %H:%M:%S")
    return result