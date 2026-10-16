
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html")

    full_name = request.POST.get("full_name", "").strip()
    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "")
    confirm_password = request.POST.get("confirm_password", "")

    if not all([full_name, email, password, confirm_password]):
        messages.error(request, "Please fill in all fields.")
        return render(request, "signup.html")

    if password != confirm_password:
        messages.error(request, "Passwords do not match.")
        return render(request, "signup.html")

    if len(password) < 8:
        messages.error(
            request,
            "Password must contain at least 8 characters."
        )
        return render(request, "signup.html")

    if User.objects.filter(email__iexact=email).exists():
        messages.error(
            request,
            "An account with this email already exists."
        )
        return render(request, "signup.html")

    try:
        User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=full_name,
        )
    except IntegrityError:
        messages.error(
            request,
            "Unable to create the account. Please try again."
        )
        return render(request, "signup.html")

    messages.success(
        request,
        "Account created successfully! You can now log in."
    )
    return redirect("login")


def login_view(request):
    if request.method == "GET":
        return render(request, "login.html")

    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "")

    if not email or not password:
        messages.error(
            request,
            "Please enter your email and password."
        )
        return render(request, "login.html")

    user = authenticate(
        request,
        username=email,
        password=password,
    )

    if user is not None:
        login(request, user)
        messages.success(request, "Login successful!")
        return redirect("student_dashboard")

    messages.error(request, "Invalid email or password.")
    return render(request, "login.html")


def logout_view(request):
    logout(request)
    messages.success(request, "You have logged out successfully.")
    return redirect("home")
