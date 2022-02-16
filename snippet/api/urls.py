from django.urls import path
from snippet.api import views

app_name = 'snippet_api'

urlpatterns = [
  path('create/', views.snippet_api_create_view, name = 'create_snippet'),
]