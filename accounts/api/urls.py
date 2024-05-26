from django.urls import path
from accounts.api import views as api_views
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    path('v1/application/', api_views.ApplicationView.as_view()),
    path('v1/profile/', api_views.ProfileView.as_view()),
]