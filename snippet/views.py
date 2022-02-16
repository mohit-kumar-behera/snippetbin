from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required(login_url = 'account:login')
def snippet_view(request):
  return render(request, 'snippet/snippet.html')
