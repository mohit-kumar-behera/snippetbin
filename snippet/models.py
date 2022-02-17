from django.db import models
from django.contrib.auth import get_user_model

from pytz import timezone
from snippet.utils import find_datetime_delta
import datetime
import uuid

User = get_user_model()

class Snippet(models.Model):
  id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)
  user = models.ForeignKey(User, on_delete = models.CASCADE)
  title = models.CharField(verbose_name = 'Title', max_length = 255)
  snippet = models.TextField(verbose_name = 'Snippet')
  is_encrypted = models.BooleanField(verbose_name = 'Is Encrypted', default = False)
  has_expiry = models.BooleanField(verbose_name = 'Has Expiry', default = False)
  created_at = models.DateTimeField(auto_now_add = True)
  expiration_date = models.DateTimeField(blank = True, null = True)
  expired = models.BooleanField(default = False, blank = True, null = True)

  def __str__(self):
    return str(self.id)
  
  def extract_delta_datetime(self):
    now = datetime.datetime.now()
    created_at = self.created_at

    # Indian Standard Time (+5:30)
    created_at = created_at + datetime.timedelta(hours = 5, minutes = 30)

    start_tz = created_at.replace(tzinfo = timezone('UTC'))
    end_tz = now.replace(tzinfo = timezone('UTC'))

    val, show_type = find_datetime_delta(start_tz, end_tz)
    
    if show_type:
      show_type = show_type if val == 1 else show_type + 's'

    result = f'{val} {show_type} ago' if show_type else f'{val}'
    return result
  
  def if_has_expired(self):
    flag = False
    
    if self.has_expiry:
      now = datetime.datetime.now()
      created_at = self.created_at
      expiration_date = self.expiration_date

      start_tz = created_at.replace(tzinfo = timezone('UTC'))
      now_tz = now.replace(tzinfo = timezone('UTC'))

      # """ REMOVE AFTER TESTING """
      # now_tz = now_tz + datetime.timedelta(days = 1)
      
      if not expiration_date:
        expire_tz = start_tz + datetime.timedelta(days = 1)
      else:
        expire_tz = expiration_date.replace(tzinfo = timezone('UTC'))

      if now_tz > expire_tz:
        flag = True      
    return flag
