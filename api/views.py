from django.contrib.auth import authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_403_FORBIDDEN
)
from rest_framework.response import Response


from .serializers import *


from .authentication import *

from rest_framework import generics, views
from django.db.models import Q
from django.db.utils import IntegrityError

@api_view(["POST"])
@permission_classes((AllowAny,))
def signin(request):
    serializer = UserSigninSerializer(data = request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


    user = authenticate(
        username = serializer.data['email'],
        password = serializer.data['password'] 
    )
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)

        
    token, _ = Token.objects.get_or_create(user = user)

    return Response({
        'token': token.key,
        'spec': user.profile.spec
    }, status=HTTP_200_OK)




@api_view(["DELETE"])
def token_destroyed(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({'detail': 'Success logout'}, status=HTTP_200_OK)