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
from accounts.forms import UserEditForm
from .forms import AdminProfileEditForm
from .models import Group
from django.shortcuts import get_object_or_404



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


@method_decorator(admin_only, name="dispatch")
class TeacherEditView(LoginRequiredMixin, View):

    def post(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(User, pk=pk)
        user_form = UserEditForm(instance=teacher, data=request.POST)
        profile_form = AdminProfileEditForm(instance=teacher.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.username = user.email
            user.save()

            group = profile_form.cleaned_data.get("group")
            profile = profile_form.save()

            if group.owner and group.owner != user:
                messages.error(request, f"У группы {group.name} уже есть учитель!")
                return redirect(reverse("teacher", kwargs={"pk": pk}))

            group.owner = profile.user
            group.save()

            messages.success(request, "Пользователь успешно изменен!")

        return redirect(reverse("teacher", kwargs={"pk": pk}))

    def get(self, request, pk, *args, **kwargs):
        teacher = get_object_or_404(User, pk=pk)
        user_form = UserEditForm(instance=teacher)
        profile_form = AdminProfileEditForm(instance=teacher.profile)

        teacher_group = teacher.study_groups.first()
        groups = Group.objects.all()

        return render(request, "study/teacher-edit.html", {
            "user_form": user_form,
            "profile_form": profile_form,
            "teacher_group": teacher_group,
            "groups": groups,
            "teacher": teacher,
        })


def delete_teacher(request, pk):

    teacher = get_object_or_404(User, pk=pk)
    username = teacher.username
    teacher.delete()
    messages.success(request, f"Учитель {username} удален!")

    return redirect(reverse("teachers"))
