from django.contrib import admin
from home.models import TinyURL

class TinyURLAdmin(admin.ModelAdmin):
  list_display = ('snippet', 'shorten_url', 'created_at')
  ordering = ('-created_at',)

admin.site.register(TinyURL, TinyURLAdmin)
