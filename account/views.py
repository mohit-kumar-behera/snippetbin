from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from account.decorators import allow_unauthorized_user

User = get_user_model()

@allow_unauthorized_user(redirect_url = 'home:home')
def signup_view(request):
  if request.POST:
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
      User.objects.get(email = email)
    except User.DoesNotExist:
      """ Continue with signup """
      user = User.objects.create_user(email, password)
      user.name = name
      user.save()
      messages.success(request, 'Account creation was successful. Please login to continue')
      return redirect('account:login')
    else:
      """ User already exists with this email """
      messages.error(request, 'Account with this email already exists')
      return redirect('account:signup')
  return render(request, 'account/signup.html')

@allow_unauthorized_user(redirect_url = 'home:home')
def login_view(request):
  redirect_to = request.GET.get('next', 'home:home')
  
  if request.POST:
    email = request.POST.get('email')
    password = request.POST.get('password')
    authenticated_user = authenticate(request, email=email, password=password)
    
    if authenticated_user is None:
      messages.error(request, 'Either email or password is incorrect')
      return redirect('account:login')

    login(request, authenticated_user)
    return redirect(redirect_to)
  return render(request, 'account/login.html')


@login_required(login_url = 'account:login')
def logout_view(request):
  logout(request)
  return redirect('home:home')