from study import views
from django.urls import path


urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("teachers/", views.TeachersListView.as_view(), name="teachers"),
    path("teacher/<int:pk>/", views.TeacherEditView.as_view(), name="teacher"),
    path("teacher/delete/<int:pk>/", views.delete_teacher, name="teacher-delete"),
    path("teacher/add/", views.TeacherCreateView.as_view(), name="teacher-add"),

    path("students/", views.StudentsListView.as_view(), name="students"),
    path("student/<int:pk>/", views.StudentEditView.as_view(), name="student"),
    path("student/delete/<int:pk>/", views.delete_student, name="student-delete"),
    path("student/add/", views.StudentCreateView.as_view(), name="student-add"),

    path("applications/", views.ApplicationsListView.as_view(), name="applications"),
    path("application/<int:pk>/", views.ApplicationView.as_view(), name="application"),
    path("application/delete/<int:pk>/", views.delete_application, name="application-delete"),

    path("groups/", views.GroupsListView.as_view(), name="groups"),
    path("group/<int:pk>/", views.GroupEditView.as_view(), name="group"),
    path("group/delete/<int:pk>/", views.delete_group, name="group-delete"),
    path("group/add/", views.GroupCreateView.as_view(), name="group-add"),

    path("subjects/", views.SubjectsListView.as_view(), name="subjects"),
    path("subject/<int:pk>/", views.SubjectEditView.as_view(), name="subject"),
    path("subject/delete/<int:pk>/", views.delete_subject, name="subject-delete"),
    path("subject/add/", views.SubjectCreateView.as_view(), name="subject-add"),

    path("lessons/", views.LessonsListView.as_view(), name="lessons"),
    path("lesson/<int:pk>/", views.LessonEditView.as_view(), name="lesson"),
    path("lesson/add/", views.LessonCreateView.as_view(), name="lesson-add"),
]
