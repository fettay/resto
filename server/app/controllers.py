from app.serializers import UserSerializer

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes


@api_view(['POST'])
def login(request, format=None):
    if request.user.is_authenticated:
        return Response(UserSerializer(request.user).data)
    
    user = authenticate(username=request.data['email'], password=request.data['password'])
    if user is None:
        return Response({'error': 'User cannot be found'}, 401)

    token, created = Token.objects.get_or_create(user=user)
    response_data = UserSerializer(user).data
    response_data['token'] = token.key
    return Response(response_data)
    


# @api_view(['GET'])
# @authentication_classes([SessionAuthentication])
# @permission_classes([IsAuthenticated])
# def me(request, format=None):
#     content = {
#         'user': unicode(request.user),  # `django.contrib.auth.User` instance.
#         'auth': unicode(request.auth),  # None
#     }
#     return Response(content)

# Create your views here.
