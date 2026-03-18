from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.urls import reverse
from django.contrib.auth import login,logout


def user_signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(reverse("user_login"))
    context = {"form":form}
    return render(request,"user/user_signup.html",context)
    

def user_login(request):
    form = AuthenticationForm(request,request.POST or None)
    if form.is_valid():
        login(request,form.get_user())
        return  redirect(reverse("todo_list"))
    context ={"form":form}
    return render(request,"user/user_login.html",context)

def user_logout(request):
    logout(request)
    return redirect(reverse("todo_list"))