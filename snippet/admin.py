from django.contrib import admin
from snippet.models import Snippet

class SnippetAdmin(admin.ModelAdmin):
  list_display = ('user', 'title', 'created_at')
  search_fields = ('title',)
  ordering = ('-created_at',)

admin.site.register(Snippet, SnippetAdmin)