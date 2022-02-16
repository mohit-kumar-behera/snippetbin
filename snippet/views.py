from django.shortcuts import render

def snippet_view(request):
  return render(request, 'snippet/snippet.html')
