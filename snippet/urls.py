from django.urls import path
from snippet import views

app_name = 'snippet'

urlpatterns = [
  path('', views.snippet_create_view, name = 'snippet'),
  path('<str:sid>/', views.snippet_detail_view, name = 'snippet_detail'),
  path('<str:sid>/edit/', views.snippet_edit_view, name = 'snippet_edit'),
  path('<str:sid>/statistics/', views.snippet_statistics_view, name = 'snippet_statitics')
]