from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import LoginForm, RegisterForm, AddWebsiteForm, EditWebsiteForm
from .models import Website
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_session
from django.db import IntegrityError
User = get_user_model()
# Create your views here.

def index(request):
    user = request.user
    websites = Website.objects.filter(user=user)
    # websites = [websites] if len(websites) == 1 else websites
    if not user.is_authenticated:
        return HttpResponseRedirect('/login/')
    return render(request, 'index.html', {'websites':websites, 'username':user.username})


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            print(form.cleaned_data["username"], form.cleaned_data["password"])
            user = authenticate(username=form.cleaned_data["username"], password=form.cleaned_data["password"])
            if user is None:
                form.add_error(None, "Invalid Credentials")
                print("Added error moron")
            else:
                print("Successfully logged in")
                login_session(request, user)
                return HttpResponseRedirect("/")
    else:
        form = RegisterForm()
    return render(request, 'login.html', {"form":form})

def register(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect("/")

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data["username"], email=form.cleaned_data["email"],
                        password=form.cleaned_data["password"])
            try:
                user.save()
                print(user)
                return HttpResponseRedirect("/")
            except IntegrityError:
                form.add_error(None, "User with similiar credentials already exists")

    else:
        form = RegisterForm()
    return render(request, 'register.html', {"form":form})

def addwebsite(request):
    user = request.user

    if not user.is_authenticated:
        return HttpResponseRedirect('/login/')
    if request.method == "POST":
        form = AddWebsiteForm(request.POST)
        if form.is_valid():
            w = Website(user=user, name=form.cleaned_data["name"], password=form.cleaned_data["password"], username=form.cleaned_data["username"], URL=form.cleaned_data["URL"])
            w.save()

    return HttpResponseRedirect('/')

def editwebsite(request):

    user = request.user
    print("edit is called!")
    print(request.POST)
    if not user.is_authenticated:
        return HttpResponseRedirect('/login/')
    if request.method == "POST":
        form = EditWebsiteForm(request.POST)
        if form.is_valid():
            print("form valid")
            print(form.cleaned_data)
            wb = Website.objects.get(id=form.cleaned_data["id"])
            wb.username = form.cleaned_data["username"]
            wb.password = form.cleaned_data["password"]
            wb.URL = form.cleaned_data["URL"]
            wb.name = form.cleaned_data["name"]
            wb.save()

        else:
            print(form)
    return HttpResponseRedirect('/')