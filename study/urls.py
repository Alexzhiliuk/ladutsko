from study import views
from django.urls import path


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("teachers/", views.TeachersListView.as_view(), name="teachers"),
    path("teacher/<int:pk>/", views.TeacherEditView.as_view(), name="teacher"),
    path("teacher/delete/<int:pk>/", views.delete_teacher, name="teacher-delete"),
    path("teacher/add/", views.TeacherCreateView.as_view(), name="teacher-add"),
]
