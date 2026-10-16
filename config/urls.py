
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from accounts.views import signup, login_view, logout_view


def home(request):
    return render(request, "home.html")


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("signup/", signup, name="signup"),
    path("login/", login_view, name="login"),
    path("passes/", include("passes.urls")),
    path("logout/", logout_view, name="logout"),
]
