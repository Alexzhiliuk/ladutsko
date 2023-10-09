from accounts import views
from django.urls import path

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('application/', views.ApplicationView.as_view(), name='application'),
]