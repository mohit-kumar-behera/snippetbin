from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from account.decorators import check_edit_authorization

from snippet.models import Snippet
from snippet.decorators import is_valid_uuid, check_expiry

import socket

@login_required(login_url = 'account:login')
def snippet_create_view(request):
  return render(request, 'snippet/snippet.html')


@check_expiry
def snippet_detail_view(request, sid):
  try:
    snippet_obj = Snippet.objects.get(id = sid)
  except Snippet.DoesNotExist:
    messages.info(request, 'No such Snippet exists for the given ID')
    return redirect('home:home')
  except:
    messages.error(request, 'Not a Valid UUID')
    return redirect('home:home')

  hostname = socket.gethostname()
  ip_address = socket.gethostbyname(hostname)

  found_tracker_of_ip = snippet_obj.snipettracker_set.filter(ip_addr = ip_address).first()
  
  if found_tracker_of_ip:
    """ UPDATE TRACKER RESULT FOR THAT IP """
    found_tracker_of_ip.count = found_tracker_of_ip.count + 1
    found_tracker_of_ip.save()
  else:
    """ CREATE TRACKER RESULT FOR THAT IP """
    snippet_obj.snipettracker_set.create(
      hostname = hostname,
      ip_addr = ip_address,
      count = 1,
    )

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


@login_required(login_url = 'account:login')
def snippet_statistics_view(request, sid):
  try:
    snippet_obj = Snippet.objects.get(id = sid)
  except Snippet.DoesNotExist:
    messages.error(request, f'No snippet with id {sid} exists')
    return redirect('home:home')
  except:
    messages.error(request, f'No snippet with id {sid} exists')
    return redirect('home:home')
  
  stats = snippet_obj.snipettracker_set.all().order_by('-viewed_at')
  context = {'stats': stats}
  return render(request, 'snippet/snippet-stats.html', context)