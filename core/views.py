from django.shortcuts import render, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import *
import requests
import json


def login_view(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            cd = login_form.cleaned_data

            user = authenticate(username=cd['username'], password=cd['password'])
            if user.is_active:
                if 'remember' not in request.POST:
                    request.session.set_expiry(0)
                    request.session.modified = True
                login(request, user)
                return redirect(index)
            else:
                return render(request, 'disable.html')
    else:
        if request.user.is_authenticated:
            return redirect(index)
        login_form = LoginForm()
    return render(request, 'login.html', {'form': login_form})


def logout_view(request):
    logout(request)
    return redirect(login_view)



@login_required(login_url='/login/')
def index(request):
    if request.user.is_superuser:
        logout(request)
        return redirect(login_view)
    
    r = requests.get(f"http://176.62.187.250/logist.php")
    
    try:
        data = json.loads(r.text)
    except json.decoder.JSONDecodeError:
        r = requests.get(f"http://176.62.187.250/logist.php")
        data = json.loads(r.text)

    return render(request, 'orders.html', {"datas": data})


@login_required(login_url='/login/')
def create_route(request):
    if request.method == "POST":
        Route.objects.create(author_id=request.user.logist.id, driver_id = request.POST["driver"])
        return redirect(routes)
    return render(request, 'new-route.html', {"drivers": Driver.objects.filter(is_free=True)})


@login_required(login_url='/login/')
def routes(request):
    return render(request, 'routes.html', {"routes": Route.objects.filter(author=request.user.logist)})