from django.db import models
from snippet.models import Snippet
import uuid

class TinyURL(models.Model):
  id = models.UUIDField(default = uuid.uuid4, unique = True, primary_key = True, editable = False)
  snippet = models.OneToOneField(Snippet, on_delete = models.CASCADE)
  original_url = models.URLField(verbose_name = 'URL Field')
  shorten_url = models.URLField(verbose_name = 'Shorten URL')
  created_at = models.DateTimeField(auto_now_add = True)

  def __str__(self):
    return self.shorten_url
