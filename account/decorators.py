from django.shortcuts import redirect

def allow_unauthorized_user(redirect_url):
  def decorator(view_func):
    def wrapper_func(request, *args, **kwargs):
      if request.user.is_authenticated:
        return redirect(redirect_url)
      return view_func(request, *args, **kwargs)
    return wrapper_func
  return decorator