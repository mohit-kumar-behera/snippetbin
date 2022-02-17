from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from account.decorators import check_edit_authorization


@login_required(login_url = 'account:login')
def snippet_create_view(request):
  return render(request, 'snippet/snippet.html')


def snippet_detail_view(request, sid):
  return render(request, 'snippet/snippet-detail.html')


@login_required(login_url = 'account:login')
@check_edit_authorization
def snippet_edit_view(request, sid):
  return render(request, 'snippet/snippet-edit.html')