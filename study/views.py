from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.contrib import messages


class IndexView(LoginRequiredMixin, View):
    menu = {
        "admin": {
            "Пользователи": {
                "Учителя": "#",
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

