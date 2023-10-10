from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from .decorators.is_admin import admin_only


class IndexView(LoginRequiredMixin, View):
    menu = {
        "admin": {
            "Пользователи": {
                "Учителя": reverse_lazy("teachers"),
                "Ученики": "#",
            },
            "Заявки": "#",
            "Группы": "#",
            "Предметы": "#",
            "Уроки": "#",
            "Тесты": "#",
            "Вопросы": "#",
        }
    }

    def get(self, request, *args, **kwargs):

        user = request.user
        if user.profile.type == 1:
            return render(request, "study/index.html", {"menu": self.menu["admin"]})


@method_decorator(admin_only, name="dispatch")
class TeachersListView(LoginRequiredMixin, ListView):
    model = User
    context_object_name = "objects"
    template_name = "study/teachers.html"

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(profile__type=2)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
