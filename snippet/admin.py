from django.contrib import admin
from snippet.models import Snippet, SnipetTracker

class SnippetAdmin(admin.ModelAdmin):
  list_display = ('user', 'title', 'created_at')
  search_fields = ('title',)
  ordering = ('-created_at',)


class SnipetTrackerAdmin(admin.ModelAdmin):
  list_display = ('snippet', 'ip_addr', 'count')
  ordering = ('-viewed_at',)


admin.site.register(Snippet, SnippetAdmin)
admin.site.register(SnipetTracker, SnipetTrackerAdmin)