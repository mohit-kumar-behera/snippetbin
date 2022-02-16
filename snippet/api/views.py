from django.urls import reverse
from django.db import transaction

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from home.models import TinyURL
from snippet.models import Snippet
from snippet.api.serializers import SnippetSerializer
import jwt
import requests

ENDPOINT_URL = 'https://api.shrtco.de/v2/shorten'

@api_view(['POST'])
@transaction.atomic
def snippet_api_create_view(request):
  if request.method == 'POST':
    data_obj = request.data
    
    title = data_obj.get('title')
    snippet = data_obj.get('snippet')
    expiry = data_obj.get('expiry').lower()
    expiry = False if expiry == 'never' else True
    is_encrypted = data_obj.get('isEncrypted', False)
    snippet_is_url = data_obj.get('is_url', False)

    if is_encrypted:
      encryption_key = data_obj.get('encryption-key')
      encoded_jwt = jwt.encode({"snippet": snippet}, encryption_key, algorithm="HS256")
      snippet = encoded_jwt
  
    try:
      snippet_obj = Snippet.objects.create(
        user = request.user,
        title = title,
        snippet = snippet,
        has_expiry = expiry,
        is_encrypted = is_encrypted
      )
    except:
      response_obj = {'success': False, 'data': {'error': 'Something went wrong'}}
      return Response(response_obj, status = status.HTTP_400_BAD_REQUEST)
    else:
      original_url = snippet if snippet_is_url else request.build_absolute_uri(reverse('snippet:snippet_detail', args = (snippet_obj.id,)))

      params = {'url': original_url}
      res = requests.get(url = ENDPOINT_URL, params = params)
      res_data = res.json()

      TinyURL.objects.create(
        snippet = snippet_obj,
        original_url = original_url,
        shorten_url = res_data['result']['full_short_link']
      )
      
      serializer = SnippetSerializer(snippet_obj, many = False)
      response_obj = {
        'success': True,
        'redirect_url': original_url,
        'data': serializer.data
      }
      return Response(response_obj, status = status.HTTP_201_CREATED)

  response_obj = {'success': False, 'data': {'error': 'Method not allowed'}}
  return Response(response_obj, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def snippet_api_detail_view(request, sid):
  if request.method == 'GET':
    try:
      snippet_obj = Snippet.objects.get(id = sid)
    except Snippet.DoesNotExist:
      response_obj = {'success': False, 'data': {'error': 'Sorry, No data found'}}
      return Response(response_obj, status = status.HTTP_404_NOT_FOUND)
    except:
      response_obj = {'success': False, 'data': {'error': 'Something went wrong'}}
      return Response(response_obj, status = status.HTTP_400_BAD_REQUEST)
    else:
      serializer = SnippetSerializer(snippet_obj, many = False)
      response_obj = {
        'success': True,
        'data': serializer.data
      }
      return Response(response_obj, status = status.HTTP_200_OK)

  response_obj = {'success': False, 'data': {'error': 'Method not allowed'}}
  return Response(response_obj, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def snippet_decrypt_api_view(request):
  if request.method == 'POST':
    data_obj = request.data
    encrypted_data = data_obj.get('data')
    encrypted_key = data_obj.get('key')
    try:
      decoded_jwt = jwt.decode(encrypted_data, encrypted_key, algorithms=["HS256"])
    except:
      response_obj = {'success': False, 'data': {'error': 'Provided key is invalid'}}
    else:
      response_obj = {'success': True, 'data': decoded_jwt}
    finally:
      return Response(response_obj, status = status.HTTP_200_OK)
  response_obj = {'success': False, 'data': {'error': 'Method not allowed'}}
  return Response(response_obj, status = status.HTTP_405_METHOD_NOT_ALLOWED)
