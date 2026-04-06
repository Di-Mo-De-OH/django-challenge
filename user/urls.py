from django.urls import path
from .import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("signup/",views.UserSignupView.as_view(),name="user-signup"),
    path("login/",views.UserLoginView.as_view(),name="user-login"),
    path("user/<int:pk>/",views.UserDetailView.as_view(),name="user-details"),
    path('logout/', LogoutView.as_view(), name='user-logout'),

]