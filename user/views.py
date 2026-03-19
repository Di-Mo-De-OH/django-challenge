from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.contrib.auth import login,logout
from django.conf import settings


def user_signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.SIGNUP_REDIRECT_URL)
    context = {"form":form}
    return render(request,"user/user_signup.html",context)
    

def user_login(request):
    form = AuthenticationForm(request,request.POST or None)
    if form.is_valid():
        login(request,form.get_user())
        return  redirect(settings.LOGIN_REDIRECT_URL)
    context ={"form":form}
    return render(request,"user/user_login.html",context)
