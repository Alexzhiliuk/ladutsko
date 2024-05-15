from django.urls import path
from accounts.api import views as api_views
from rest_framework import routers
from rest_framework.authtoken import views

router = routers.DefaultRouter()

urlpatterns = [
    path('v1/application/', api_views.ApplicationView.as_view(), name="application-view"),
    path('v1/profile/', api_views.ProfileView.as_view(), name="profile-view"),
    path('v1/logout/', api_views.LogoutView.as_view(), name="api-logout-view"),
    path('v1/api-token-auth/', views.obtain_auth_token)
]