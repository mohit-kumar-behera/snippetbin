from django.urls import path
from snippet import views

app_name = 'snippet'

urlpatterns = [
  path('', views.snippet_create_view, name = 'snippet'),
  path('<str:sid>/', views.snippet_detail_view, name = 'snippet_detail')
]