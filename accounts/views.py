from django.shortcuts import render
from django.views import View
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.contrib import messages


class LoginView(View):
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is None:
                messages.error(request, "Неверный логин или пароль!")
                return render(request, "accounts/login.html", {"form": form})

            if not user.is_active:
                messages.error(request, "Аккаунт заблокирован!")
                return render(request, "accounts/login.html", {"form": form})

            login(request, user)
            return HttpResponse("Welcome! Authenticated successfully")

        return render(request, "accounts/login.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})
