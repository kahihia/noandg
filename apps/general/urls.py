from django.urls import path

from apps.general import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('api/v1/accounts/login/', views.CustomAuthToken.as_view(), name='api_login'),
]
