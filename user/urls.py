from django.urls import path

from . import views
from user.views import UserSignUp

urlpatterns = [
    path("signup/", views.UserSignUp.as_view(), name="user_signup"),
    path("login/", views.LoginView.as_view(), name="user_login"),
    path("verify/", UserSignUp.verify_email, name="verify"),
]
