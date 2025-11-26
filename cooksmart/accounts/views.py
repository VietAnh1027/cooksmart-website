from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login
from .forms import Registerform

# Create your views here. ACCOUNTS
def register(request):
    if request.method == "POST":
        form = Registerform(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name = form.cleaned_data['first_name'],
                last_name = form.cleaned_data['last_name']
            )
            user.is_staff = False
            user.is_superuser = False
            user.save()
            login(request, user)
            return redirect("/")
    else:
        form = Registerform()
    return render(request, "register.html", {"form":form})

def admin_page(request):
    return HttpResponse("This is ADMIN page!")