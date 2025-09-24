from django.urls import path

from src.website.views.adminlte.views import MainPageView

urlpatterns = [
    path("home/", MainPageView.as_view(), name="main_page"),
]
