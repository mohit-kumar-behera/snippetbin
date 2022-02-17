from rest_framework import serializers
from snippet.models import Snippet
from account.serializers import UserSerializer
from home.serializers import TinyURLSerializer

from pytz import timezone
from snippet.utils import find_datetime_delta

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
    now = datetime.datetime.now()
    created_at = snippet.created_at

    start_tz = created_at.replace(tzinfo = timezone('UTC'))
    end_tz = now.replace(tzinfo = timezone('UTC'))

    val, show_type = find_datetime_delta(start_tz, end_tz)
    
    if show_type:
      show_type = show_type if val == 1 else show_type + 's'

    result = f'{val} {show_type} ago' if show_type else f'{val}'
    return result
