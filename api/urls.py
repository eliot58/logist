from django.urls import path
from .views import *
from django.urls import path

urlpatterns = [
    path('signin/', signin),
    path('logout/', token_destroyed),
]
