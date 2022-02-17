from datetime import datetime
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

    temp_snippet = snippet

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
      original_url = request.build_absolute_uri(reverse('snippet:snippet_detail', args = (snippet_obj.id,)))

      if snippet_is_url:
        url = temp_snippet

      params = {'url': url}
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
      response_obj = {'success': False, 'data': {'error': 'No such Snippet exists for the given ID'}}
      return Response(response_obj, status = status.HTTP_404_NOT_FOUND)
    except:
      response_obj = {'success': False, 'data': {'error': 'Not a Valid UUID'}}
      return Response(response_obj, status = status.HTTP_400_BAD_REQUEST)
    else:
      serializer = SnippetSerializer(snippet_obj, many = False)
      
      is_other_user = None
      logged_in_user = request.user if request.user.is_authenticated else None
      if not logged_in_user or logged_in_user.username != snippet_obj.user.username:
        is_other_user = True
      else:
        is_other_user = False
        
      response_obj = {
        'success': True,
        'is_other_user': is_other_user,
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


@api_view(['GET'])
def all_snippet_api_view(request):
  if request.method == 'GET':
    start = int(request.GET.get('start', None))
    end = int(request.GET.get('end', None))
    
    if start == None or end == None:
      snippets = Snippet.objects.all().order_by('-created_at')
    else:
      snippets = Snippet.objects.all().order_by('-created_at')[start:end]

    serializer = SnippetSerializer(snippets, many = True)

    response_obj = {'success': True, 'data': serializer.data}
    return Response(response_obj, status = status.HTTP_200_OK)
  response_obj = {'success': False, 'data': {'error': 'Method not allowed'}}
  return Response(response_obj, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def snippet_api_edit_view(request, sid):
  if request.method == 'POST':
    try:
      snippet_obj = Snippet.objects.get(id = sid)
    except Snippet.DoesNotExist:
      response_obj = {'success': False, 'data': {'error': 'Snippet with this ID was not found'}}
      return Response(response_obj, status = status.HTTP_404_NOT_FOUND)
    
    data_obj = request.data
    expiration_date = data_obj.get('renew-expiration', None)
    
    expiration_date_dtm = datetime.strptime(expiration_date, '%Y-%m-%d')
    now = datetime.now()

    expiration_date = expiration_date_dtm if expiration_date_dtm > now else None

    if not expiration_date:
      return Response({'success': False, 'data': {'error': 'Expiration Date can\'t be any date in past'}}, status = status.HTTP_200_OK)

    snippet_obj.expiration_date = expiration_date
    snippet_obj.has_expiry = True
    snippet_obj.save()

    serializer = SnippetSerializer(snippet_obj, many = False)
    response_obj = {'success': True, 'data': serializer.data}
    return Response(response_obj, status = status.HTTP_200_OK)
  response_obj = {'success': False, 'data': {'error': 'Method not allowed'}}
  return Response(response_obj, status = status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def snippet_api_delete_view(request, sid):
  if request.method == 'POST':
    try:
      snippet = Snippet.objects.get(id = sid)
    except Snippet.DoesNotExist:
      response_obj = {'success': False, 'data': {'error': 'Snippet with this ID was not found'}}
      return Response(response_obj, status = status.HTTP_404_NOT_FOUND)
    
    snippet.delete()
    redirect_url = request.build_absolute_uri(reverse('home:dashboard', args = (snippet.user.username,)))
    response_obj = {
      'success': True, 
      'redirect_url': redirect_url, 
      'data': {'message': 'Deleted Successfully'}
    }
    return Response(response_obj, status = status.HTTP_200_OK)
 
  response_obj = {'success': False, 'data': {'error': 'Method not allowed'}}
  return Response(response_obj, status = status.HTTP_405_METHOD_NOT_ALLOWED)
