from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.decorators import check_edit_authorization

from snippet.models import Snippet
from snippet.decorators import is_valid_uuid, check_expiry


@login_required(login_url = 'account:login')
def snippet_create_view(request):
  return render(request, 'snippet/snippet.html')


@check_expiry
def snippet_detail_view(request, sid):
  return render(request, 'snippet/snippet-detail.html')

@login_required(login_url = 'account:login')
@is_valid_uuid
@check_edit_authorization
def snippet_edit_view(request, sid):
  try:
    snippet = Snippet.objects.get(id = sid)
  except Snippet.DoesNotExist:
    messages.error(request, f'No snippet with id {sid} exists')
    return redirect('home:home')
  except:
    messages.error(request, f'No snippet with id {sid} exists')
    return redirect('home:home')
  
  context = {'snippet': snippet}
  return render(request, 'snippet/snippet-edit.html', context)