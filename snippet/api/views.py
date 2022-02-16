from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(['POST'])
def snippet_api_create_view(request):
  if request.method == 'POST':
    data_obj = request.data
    return Response('done', status = status.HTTP_201_CREATED)
  return Response('not allowed', status = status.HTTP_405_METHOD_NOT_ALLOWED)