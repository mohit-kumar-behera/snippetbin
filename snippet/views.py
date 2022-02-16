from django.shortcuts import render
from django.http import HttpResponse

def snippet_view(request):
  return HttpResponse('SNIPPET PAGE')
