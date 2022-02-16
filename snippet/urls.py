from django.urls import path
from snippet import views

app_name = 'snippet'

urlpatterns = [
  path('', views.snippet_view, name = 'snippet')
]