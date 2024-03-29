from django.contrib.auth import authenticate, logout
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from rest_framework import views

from .serializers import *

from django.db.models import Q
from .authentication import *

from datetime import datetime

@api_view(["POST"])
@permission_classes((AllowAny,))
def signin(request):
    serializer = UserSigninSerializer(data = request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)


    user = authenticate(
        username = serializer.data["login"],
        password = serializer.data["password"] 
    )
    if not user:
        return Response({"detail": "Invalid Credentials or activate account"}, status=HTTP_404_NOT_FOUND)

        
    token, _ = Token.objects.get_or_create(user = user)

    return Response({
        "token": token.key
    }, status=HTTP_200_OK)


@api_view(["DELETE"])
def token_destroyed(request):
    request.user.auth_token.delete()
    logout(request)
    return Response({"detail": "Success logout"}, status=HTTP_200_OK)

@api_view(["POST"])
def order_reponse(request, id):
    for file in request.FILES.getlist("files"):
        FileModel.objects.create(order_id=id, file = file)
    route = Route.objects.get(Q(driver_id=request.user.driver.id) & Q(is_finish=False))
    order = Order.objects.get(id=id)
    order.response = True
    order.save()
    c = 0
    for order in route.orders.all():
        if order.response:
            c += 1


    if c == len(route.orders.all()):
        route.is_finish = True
        route.save()
        request.user.driver.is_free = True
        request.user.driver.save()

    return Response({"detail": "Success"}, status=HTTP_200_OK)


@api_view(["POST"])
def set_location(request):
    serializer = LocationSerializer(data = request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status = HTTP_400_BAD_REQUEST)
    
    d = request.user.driver
    d.last_pos = f"{serializer.data['latitude']} {serializer.data['longitude']}"
    d.last_post_date_time = datetime.now()
    d.save()
    return Response({"detail": "Success"}, status=HTTP_200_OK)


class RouteView(views.APIView):
    def get(self, request):
        try:
            serializer = RouteSerializer(Route.objects.get(Q(driver_id=request.user.driver.id) & Q(is_finish=False)))
        except Route.DoesNotExist:
            return Response({"error": "Route does not exist"}, status=HTTP_404_NOT_FOUND)
        return Response(serializer.data)
