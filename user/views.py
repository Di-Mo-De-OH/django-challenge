from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def user_signup(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect(settings.SIGNUP_REDIRECT_URL)
    context = {"form": form}
    return render(request, "user/user_signup.html", context)


def user_login(request):
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        login(request, form.get_user())
        return redirect(settings.LOGIN_REDIRECT_URL)
    context = {"form": form}
    return render(request, "user/user_login.html", context)
