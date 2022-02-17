from django.shortcuts import redirect
from django.contrib import messages
import uuid

from snippet.models import Snippet

def is_valid_uuid(view_func):
  def wrapper(request, sid, *args, **kwargs):
    try:
      uuid.UUID(str(sid))
      return view_func(request, sid, *args, **kwargs)
    except ValueError:
      messages.error(request, 'Not a Valid Snippet ID')
      return redirect('home:home')
  return wrapper


def check_expiry(view_func):
  def wrapper(request, sid, *args, **kwargs):
    try:
      snippet_obj = Snippet.objects.get(id = sid)
    except Snippet.DoesNotExist:
      return view_func(request, sid, *args, **kwargs)
    except:
      return view_func(request, sid, *args, **kwargs)
    
    has_expired = snippet_obj.if_has_expired()

    if has_expired:
      snippet_obj.delete()
    else:
      snippet_obj.expired = has_expired
      snippet_obj.save()

    return view_func(request, sid, *args, **kwargs)
  return wrapper
