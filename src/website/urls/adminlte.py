from django.urls import path

from src.website.views.adminlte.views import (
    MainPageView,
    AboutUsPageView,
    ContactsPageView,
    ServicePageView,
    TariffsPageView,
)

urlpatterns = [
    path("home/", MainPageView.as_view(), name="main_page"),
    path("about/", AboutUsPageView.as_view(), name="about_page"),
    path("contacts/", ContactsPageView.as_view(), name="contacts_page"),
    path("services/", ServicePageView.as_view(), name="services_page"),
    path("tariffs/", TariffsPageView.as_view(), name="tariffs_page"),
]
