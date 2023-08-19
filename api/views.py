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
from rest_framework import views

from .serializers import *

from django.db.models import Q
from .authentication import *

@api_view(["POST"])
@permission_classes((AllowAny,))
def signin(request):
    serializer = UserSigninSerializer(data = request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


    user = authenticate(
        username = serializer.data['login'],
        password = serializer.data['password'] 
    )
    if not user:
        return Response({'detail': 'Invalid Credentials or activate account'}, status=HTTP_404_NOT_FOUND)

        
    token, _ = Token.objects.get_or_create(user = user)

    return Response({
        'token': token.key
    }, status=HTTP_200_OK)


@api_view(["DELETE"])
def token_destroyed(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({'detail': 'Success logout'}, status=HTTP_200_OK)

@api_view(["POST"])
def order_reponse(request, id):
    order = Order.objects.get(id = id)
    order.response = request.FILES["file"]
    order.save()
    route = Route.objects.get(Q(driver_id=request.user.driver.id) & Q(is_finish=False))
    c = 0
    for order in route.orders.all():
        if order.response != "":
            c += 1

    if c == len(route.orders.all()):
        route.is_finish = True
        route.save()
    return Response({'detail': 'Success'}, status=HTTP_200_OK)


class RouteView(views.APIView):
    def get(self, request):
        try:
            serializer = RouteSerializer(Route.objects.get(Q(driver_id=request.user.driver.id) & Q(is_finish=False)))
        except Route.DoesNotExist:
            return Response({'error': 'Route does not exist'}, status=HTTP_404_NOT_FOUND)
        return Response(serializer.data)
