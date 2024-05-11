from django.urls import path
from study.api import views as api_views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('v1/index/', api_views.IndexView.as_view(), name="api-index"),
    path("v1/teachers/", api_views.TeachersListView.as_view(), name="api-teachers"),
    path("v1/teacher/<int:pk>/", api_views.TeacherEditView.as_view(), name="api-teacher"),
    path("v1/teacher/add/", api_views.TeacherCreateView.as_view(), name="api-teacher-add"),
    path("v1/teacher/delete/<int:pk>/", api_views.DeleteTeacherView.as_view(), name="api-teacher-delete"),

    path("v1/students/", api_views.StudentsListView.as_view(), name="api-students"),
    path("v1/student/<int:pk>/", api_views.StudentEditView.as_view(), name="api-student"),
    path("v1/student/add/", api_views.StudentCreateView.as_view(), name="api-student-add"),
    path("v1/student/delete/<int:pk>/", api_views.DeleteStudentView.as_view(), name="api-student-delete"),

    path("v1/applications/", api_views.ApplicationsListView.as_view(), name="api-applications"),
    path("v1/application/<int:pk>/", api_views.ApplicationView.as_view(), name="api-application"),
    path("v1/application/delete/<int:pk>/", api_views.DeleteApplicationView.as_view(), name="api-application-delete"),

    path("v1/groups/", api_views.GroupsListView.as_view(), name="api-groups"),
    path("v1/group/<int:pk>/", api_views.GroupEditView.as_view(), name="api-group"),
    path("v1/group/add/", api_views.GroupCreateView.as_view(), name="api-group-add"),
    path("v1/group/delete/<int:pk>/", api_views.DeleteGroupView.as_view(), name="api-group-delete"),
    path("v1/group/<int:pk>/students/", api_views.GroupStudentsListView.as_view(), name="api-group-students"),
    path("v1/group/<int:pk>/add-subject", api_views.TeacherGroupSubjectCreateView.as_view(), name="api-group-add-subject"),
    path("v1/group/<int:pk>/remove-subject", api_views.DeleteTeacherGroupSubjectView.as_view(), name="api-group-remove-subject"),
    path("v1/group/exclude-student/<int:pk>/", api_views.ExcludeStudentView.as_view(), name="api-group-exclude-student"),
    path("v1/group/student-grade/<int:pk>/", api_views.StudentGradeView.as_view(), name="api-group-student-grade"),

    path("v1/subjects/", api_views.SubjectsListView.as_view(), name="api-subjects"),
    path("v1/subject/<int:pk>/", api_views.SubjectEditView.as_view(), name="api-subject"),
    path('v1/subject/add/', api_views.SubjectCreateView.as_view(), name="api-subject-add"),
    path("v1/subject/delete/<int:pk>/", api_views.DeleteSubjectView.as_view(), name="api-subject-delete"),

    path("v1/lessons/", api_views.LessonsListView.as_view(), name="api-lessons"),
    path("v1/lesson/<int:pk>/", api_views.LessonEditView.as_view(), name="api-lesson"),
    path("v1/lesson/add/", api_views.LessonCreateView.as_view(), name="api-lesson-add"),
    path("v1/lesson/delete/<int:pk>/", api_views.DeleteLessonView.as_view(), name="api-lesson-delete"),
    path("v1/lesson/<int:pk>/add-photo/", api_views.LessonPhotoAddingView.as_view(), name="api-lesson-add-photo"),
    path("v1/lesson/<int:pk>/add-video/", api_views.LessonVideoAddingView.as_view(), name="api-lesson-add-video"),
    path("v1/lesson/<int:pk>/add-file/", api_views.LessonFileAddingView.as_view(), name="api-lesson-add-file"),
    path("v1/lesson/delete-photo/<int:pk>/", api_views.DeleteLessonPhotoView.as_view(), name="api-lesson-delete-photo"),
    path("v1/lesson/delete-video/<int:pk>/", api_views.DeleteLessonVideoView.as_view(), name="api-lesson-delete-video"),
    path("v1/lesson/delete-file/<int:pk>/", api_views.DeleteLessonFileView.as_view(), name="api-lesson-delete-file"),
    path("v1/lesson/check-work/<int:pk>/", api_views.CheckStudentWork.as_view(), name="api-lesson-check-work"),


    path("v1/tests/", api_views.TestsListView.as_view(), name="api-tests"),
    path('v1/test/<int:pk>/', api_views.TestEditView.as_view(), name="api-test"),
    path('v1/test/add/', api_views.TestCreateView.as_view(), name="api-test-add"),
    path("v1/test/delete/<int:pk>/", api_views.DeleteTestView.as_view(), name="api-test-delete"),
    path("v1/test/<int:pk>/question/add/", api_views.TestQuestionCreateView.as_view(), name="api-test-question-add"),
    path("v1/test/question/<int:pk>/", api_views.TestQuestionEditView.as_view(), name="api-test-question"),
    path("v1/test/question/<int:pk>/delete", api_views.DeleteQuestionView.as_view(), name="api-test-question-delete"),
    path("v1/test/try/<int:pk>/check/", api_views.CheckTestView.as_view(), name="api-test-try-check"),

    path("v1/question/<int:pk>/add-answer-variant/", api_views.AddAnswerVariantView.as_view(), name="api-add-answer-variant"),
    path("v1/question/<int:pk>/add-correct-text-answer/", api_views.AddCorrectTextAnswerView.as_view(), name="api-add-correct-text-answer"),
    path("v1/answer/delete/<int:pk>/", api_views.DeleteAnswerView.as_view(), name="api-answer-delete"),

    path("v1/teacher/my-group/", api_views.MyGroupListView.as_view(), name="api-my-group"),
    path("v1/teacher/my-subjects/", api_views.MySubjectsListView.as_view(), name="api-my-subjects"),
    path("v1/teacher/my-subjects/create/", api_views.MySubjectCreateView.as_view(), name="api-my-subject-create"),
    path("v1/teacher/my-subject/<int:pk>/", api_views.MySubjectEditView.as_view(), name="api-my-subject"),
    path("v1/teacher/my-lessons/", api_views.MyLessonsListView.as_view(), name="api-my-lessons"),
    path("v1/teacher/my-lessons/create/", api_views.MyLessonCreateView.as_view(), name="api-my-lesson-create"),
    path("v1/teacher/my-lesson/<int:pk>/", api_views.MyLessonEditView.as_view(), name="api-my-lesson"),
    path("v1/teacher/my-tests/", api_views.MyTestsListView.as_view(), name="api-my-tests"),

    path("v1/subject/<int:pk>/add-to-group/", api_views.AddSubjectToGroup.as_view(), name="api-add-subject-to-group"),
    path("v1/subject/<int:pk>/remove-from-group/", api_views.RemoveSubjectFromGroup.as_view(),
         name="api-remove-subject-from-group"),

    path("v1/student/subject/<int:pk>/", api_views.StudentSubjectView.as_view(), name="api-student-subject"),
    path("v1/student/lesson/<int:pk>/", api_views.StudentLessonView.as_view(), name="api-student-lesson"),
    path("v1/student/lesson/<int:pk>/individual-work/", api_views.StudentIndividualWorkView.as_view(),
         name="api/student-individual-work"),
    path("v1/student/test/<int:pk>/", api_views.StudentTestView.as_view(), name="api-student-test"),

]