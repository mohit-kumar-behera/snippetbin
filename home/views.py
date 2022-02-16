from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.exceptions import MultipleObjectsReturned

User = get_user_model()

def home_view(request):
  return render(request, 'home/home.html')


def dashboard_view(request, username):
  context = {}
  logged_in_user = request.user if request.user.is_authenticated else None

  if not logged_in_user or logged_in_user.username != username:
    context['is_other_user'] = True
  else:
    context['is_other_user'] = False
  
  try:
    user = User.objects.get(username = username)
  except User.DoesNotExist:
    messages.info(request, 'Requested user\'s profile doesnot exists')
    return redirect('home:home')
  except MultipleObjectsReturned:
    user = User.objects.filter(username = username).first()
  
  context['user'] = user
  return render(request, 'home/dashboard.html', context)
