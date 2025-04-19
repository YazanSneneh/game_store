from django.urls import path
from core.views import LoginView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]