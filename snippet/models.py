from django.db import models
from django.contrib.auth import get_user_model
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

  def __str__(self):
    return self.title
