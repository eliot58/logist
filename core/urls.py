from django.urls import path
from .views import *
from django.urls import path

urlpatterns = [
    path("", index, name = "index"),
    path("login/", login_view, name = "login_view"),
    path("logout/", logout_view, name = "logout_core_view"),
    path("routes/", routes, name = "routes"),
    path("route/<int:id>", route, name = "route"),
    path("create-route/", create_route, name = "create_route"),
    path("route/delete/<int:id>", route_delete, name = "route_delete"),
    path("set-driver/", set_driver, name = "set_driver"),
]
