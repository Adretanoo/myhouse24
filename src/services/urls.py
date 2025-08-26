from django.urls import path
from src.services import views

urlpatterns = [
    path("", views.statistics, name="statistics"),
]
