from django.urls import path
from account import views

app_name = 'account'

urlpatterns = [
  path('signup/', views.signup_view, name = 'signup'),
  path('login/', views.login_view, name = 'login'),
  path('logout/', views.logout_view, name = 'logout')
]