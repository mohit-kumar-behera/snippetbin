from django.shortcuts import redirect
from django.contrib import messages
import uuid

def is_valid_uuid(view_func):
  def wrapper(request, sid, *args, **kwargs):
    try:
      uuid.UUID(str(sid))
      return view_func(request, sid, *args, **kwargs)
    except ValueError:
      messages.error(request, 'Not a Valid Snippet ID')
      return redirect('home:home')
  return wrapper
