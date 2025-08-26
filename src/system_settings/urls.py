from django.urls import path
from src.system_settings import views

urlpatterns = [
    path(
        "payment-details/", views.PaymentDetailsView.as_view(), name="payment_details"
    ),
    path("service/", views.ServiceSettingsView.as_view(), name="service_settings"),
]
