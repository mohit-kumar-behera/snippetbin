from django.shortcuts import render

def signup_view(request):
  return render(request, 'account/signup.html')

def login_view(request):
  return render(request, 'account/login.html')
