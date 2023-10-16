from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.http import HttpResponse
from .forms import LoginForm, ApplicationForm
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
            return redirect(reverse("index"))

        return render(request, "accounts/login.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})


class ApplicationView(View):
    def post(self, request, *args, **kwargs):
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "accounts/application-sent-successfully.html")

        messages.error(request, "Неверно введены данные!")
        return render(request, "accounts/application.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = ApplicationForm()
        return render(request, "accounts/application.html", {"form": form})
