from django.urls import path
from src.system_settings import views
from src.system_settings.ajax_views import (
    PaymentItemsAjaxDatatableView,
    TariffsSettingsAjaxView,
)
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
    path("tariffs/", views.TariffsSettingsView.as_view(), name="tariffs"),
    path("tariffs/add/", views.TariffsSettingsAddView.as_view(), name="tariffs_add"),
    path(
        "tariffs/edit/<int:pk>/",
        views.TariffsSettingsEditView.as_view(),
        name="tariffs_edit",
    ),
    path(
        "tariffs/delete/<int:pk>/",
        views.TariffsSettingsDeleteView.as_view(),
        name="tariffs_delete",
    ),
    path(
        "tariffs/create/",
        views.TariffsSettingsCopyCreateView.as_view(),
        name="tariffs_copy",
    ),
    path(
        "ajax_datatable/payment_items/",
        PaymentItemsAjaxDatatableView.as_view(),
        name="ajax_payment_items",
    ),
    path(
        "ajax_datatable/tariffs//",
        TariffsSettingsAjaxView.as_view(),
        name="ajax_tariffs",
    ),
]
