from django.urls import path
from src.system_settings import views
from src.system_settings.ajax_views import PaymentItemsAjaxDatatableView
from src.system_settings.views import PaymentItemsSettingsUpdateView

urlpatterns = [
    path(
        "payment-details/", views.PaymentDetailsView.as_view(), name="payment_details"
    ),
    path("service/", views.ServiceSettingsView.as_view(), name="service_settings"),
    path("roles/", views.RolesView.as_view(), name="roles"),
    path(
        "payment-items/", views.PaymentItemsSettingsView.as_view(), name="payment_items"
    ),
    path(
        "payment-items/add/",
        views.PaymentItemsSettingsAddView.as_view(),
        name="payment_items_add",
    ),
    path(
        "payment-items/edit/<int:pk>/",
        PaymentItemsSettingsUpdateView.as_view(),
        name="payment_items_edit",
    ),
    path(
        "payment-items/delete/<int:pk>/",
        views.PaymentItemsSettingsDeleteView.as_view(),
        name="payment_items_delete",
    ),
    path(
        "ajax_datatable/payment_items/",
        PaymentItemsAjaxDatatableView.as_view(),
        name="ajax_payment_items",
    ),
]
