from django.shortcuts import redirect
from django.contrib import messages
from snippet.models import Snippet

def allow_unauthorized_user(redirect_url):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
      if request.user.is_authenticated:
        return redirect(redirect_url)
      return view_func(request, *args, **kwargs)
    return wrapper_func
  return decorator


def check_edit_authorization(view_func):
  def wrapper_func(request, sid, *args, **kwargs):
    try:
      Snippet.objects.get(user = request.user, id = sid)
    except Snippet.DoesNotExist:
      messages.warning(request, 'You don\'t have permission to edit this snippet ')
      return redirect('home:home')
    return view_func(request, sid, *args, **kwargs)
  return wrapper_func
