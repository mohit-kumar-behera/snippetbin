from django.urls import path
from snippet.api import views

app_name = 'snippet_api'

urlpatterns = [
  path('', views.all_snippet_api_view, name = 'all_snippets'),
  path('decrypt/', views.snippet_decrypt_api_view, name = 'decrypt_snippet'),
  path('create/', views.snippet_api_create_view, name = 'create_snippet'),
  path('delete/<str:sid>/', views.snippet_api_delete_view, name = 'delete_snippet'),
  path('v/<str:sid>/', views.snippet_api_detail_view, name = 'snippet_detail'),
]