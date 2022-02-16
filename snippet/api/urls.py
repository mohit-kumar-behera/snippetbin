from django.urls import path
from snippet.api import views

app_name = 'snippet_api'

urlpatterns = [
  path('decrypt/', views.snippet_decrypt_api_view, name = 'decrypt_snippet'),
  path('create/', views.snippet_api_create_view, name = 'create_snippet'),
  path('v/<str:sid>/', views.snippet_api_detail_view, name = 'snippet_detail'),
]