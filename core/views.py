from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
import requests
import json
import redis
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseForbidden, JsonResponse
from .tasks import call


def login_view(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data

            user = authenticate(username = cd["username"], password = cd["password"])
            if user.is_active:
                login(request, user)
                return redirect(index)
            else:
                return render(request, "disable.html")
    else:
        if request.user.is_authenticated:
            return redirect(index)
        login_form = LoginForm()
    return render(request, "login.html", {"form": login_form})


def logout_view(request):
    logout(request)
    return redirect(login_view)



@login_required(login_url="/login/")
def index(request):
    if request.user.is_superuser:
        logout(request)
        return redirect(login_view)
    
    re = redis.StrictRedis(
        host="127.0.0.1",
        port=6379
    )

    orders = re.get(f"orders_{request.user.username}")

    if not orders or int(request.GET.get("reload", 0)):
        r = requests.get(f"http://176.62.187.250/logist.php")
        
        try:
            orders = json.loads(r.text)
        except json.decoder.JSONDecodeError:
            r = requests.get(f"http://176.62.187.250/logist.php")
            orders = json.loads(r.text)

        re.set(f"orders_{request.user.username}", r.text, 60 * 60 * 24)

    else:
        orders = json.loads(orders)

    if request.GET.get("filter") == "work":
        filtered = list(filter(lambda item: item["s_name"] == "В производстве", orders))
    elif request.GET.get("filter") == "sklad":
        filtered = list(filter(lambda item: item["s_name"] == "На складе", orders))
    elif request.GET.get("filter") == "loaded":
        filtered = list(filter(lambda item: item["s_name"] == "Отгружен", orders))
    elif request.GET.get("filter") == "finish":
        filtered = list(filter(lambda item: item["s_name"] == "Завершен", orders))
    else:
        filtered = orders
        
    orders = sorted(filtered, key=lambda item: item["plan_date"] if item["plan_date"] != None else "", reverse = True)
    


    return render(request, "orders.html", {"orders": orders})



@login_required(login_url="/login/")
def routes(request):
    return render(request, "routes.html", {"routes": Route.objects.filter(author = request.user.logist)})


@login_required(login_url="/login/")
@require_POST
@csrf_exempt
def create_route(request):
    data = json.loads(request.body.decode())
    route = Route.objects.create(author_id=request.user.logist.id, route_link = data["route_link"])
    for value in data["orders"]:
        order = Order.objects.create(**value)
        route.orders.add(order)
    call.delay(route.id)
    return JsonResponse({"success": True})


@login_required(login_url="/login/")
@require_POST
@csrf_exempt
def set_driver(request):
    data = json.loads(request.body.decode())
    route = Route.objects.get(id=data["id"])
    route.driver_id = data["driver_id"]
    route.save()
    driver = Driver.objects.get(id=data["driver_id"])
    driver.is_free = False
    driver.save()
    return JsonResponse({"success": True})


@login_required(login_url = "/login/")
def route(request, id):
    return render(request, "route.html", {"route": Route.objects.get(id=id), "drivers": Driver.objects.filter(is_free = True)})


@login_required(login_url = "/login/")
def route_delete(request, id):
    r = Route.objects.get(id = id)
    if request.user.logist.id == r.author_id:
        r.delete()
        return redirect(routes)
    else:
        return HttpResponseForbidden()