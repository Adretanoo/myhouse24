from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import UpdateView, TemplateView
from src.system_settings.forms import (
    PaymentDetailsForm,
    ServiceSettingsFormSet,
    UnitsMeasurementFormSet,
    RolesFormSet,
)
from src.system_settings.models import (
    PaymentDetailsSettings,
    UnitsMeasurement,
    ServiceSettings,
    Roles,
    JobTitle,
)


class PaymentDetailsView(UpdateView):
    template_name = "system_settings/payment_details.html"
    form_class = PaymentDetailsForm
    success_url = reverse_lazy("payment_details")

    def get_object(self, queryset=None):
        return PaymentDetailsSettings.objects.first()


class ServiceSettingsView(TemplateView):
    template_name = "system_settings/service_settings.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["service_settings"] = ServiceSettingsFormSet(
            queryset=ServiceSettings.objects.all(),
            prefix="service_settings",
        )
        context["units_measurement"] = UnitsMeasurementFormSet(
            queryset=UnitsMeasurement.objects.all(),
            prefix="units_measurement",
        )
        return context

    def post(self, request, *args, **kwargs):
        service_settings = ServiceSettingsFormSet(
            request.POST, prefix="service_settings"
        )
        units_measurement = UnitsMeasurementFormSet(
            request.POST, prefix="units_measurement"
        )

        if service_settings.is_valid() and units_measurement.is_valid():
            service_settings.save()
            units_measurement.save()

        return redirect("service_settings")


class RolesView(TemplateView):
    template_name = "system_settings/roles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = RolesFormSet(queryset=Roles.objects.all())

        for value, label in JobTitle.choices:
            Roles.objects.get_or_create(job_title=value)
        return context

    def post(self, request, *args, **kwargs):
        roles = RolesFormSet(request.POST, queryset=Roles.objects.all())
        if roles.is_valid():
            roles.save()
        return redirect("roles")
