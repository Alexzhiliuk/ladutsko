from study import views
from django.urls import path

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("teachers/", views.TeachersListView.as_view(), name="teachers"),
    path("teacher/<int:pk>/", views.TeacherEditView.as_view(), name="teacher"),
]
