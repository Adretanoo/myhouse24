from django.db.models import Count
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    UpdateView,
    ListView,
    CreateView,
    DeleteView,
)

from src.system_settings.filters import UsersSettingsFilter
from src.system_settings.forms import (
    PaymentDetailsForm,
    ServiceSettingsFormSet,
    UnitsMeasurementFormSet,
    RolesFormSet,
    PaymentItemsSettingsForm,
    TariffsSettingsForm,
    PriceTariffSettingsFormSet,
    UserSettingsForm,
)
from src.system_settings.models import (
    PaymentDetailsSettings,
    UnitsMeasurement,
    ServiceSettings,
    Roles,
    PaymentItemsSettings,
    TariffsSettings,
    PriceTariffSettings,
)
from src.users.models import User


class PaymentDetailsView(UpdateView):
    template_name = "system_settings/payment_details.html"
    form_class = PaymentDetailsForm
    success_url = reverse_lazy("payment_details")

    def get_object(self, queryset=None):
        return PaymentDetailsSettings.objects.first()


class TariffsSettingsView(ListView):
    template_name = "system_settings/tariff/tariff_settings_table.html"
    model = TariffsSettings


class TariffsSettingsAddView(CreateView):
    template_name = "system_settings/tariff/tariff_settings_add.html"
    form_class = TariffsSettingsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tariff_service"] = PriceTariffSettingsFormSet(
            queryset=PriceTariffSettings.objects.none(),
            prefix="tariff_service",
        )
        context["services_data_json"] = list(
            ServiceSettings.objects.values("id", "units_measurement__title")
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        tariff_service = PriceTariffSettingsFormSet(
            data=request.POST, prefix="tariff_service"
        )

        if form.is_valid() and tariff_service.is_valid():
            tariff = form.save()
            instances = tariff_service.save(commit=False)
            for instance in instances:
                instance.tariff = tariff
                instance.save()
            return redirect("tariffs")
        else:
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "tariff_service": tariff_service,
                    "services_data_json": list(
                        ServiceSettings.objects.values("id", "units_measurement__title")
                    ),
                },
            )


class TariffsSettingsEditView(UpdateView):
    model = TariffsSettings
    template_name = "system_settings/tariff/tariff_settings_edit.html"
    form_class = TariffsSettingsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["tariff_service"] = PriceTariffSettingsFormSet(
            queryset=PriceTariffSettings.objects.filter(tariff=self.object),
            prefix="tariff_service",
        )
        context["services_data_json"] = list(
            ServiceSettings.objects.values("id", "units_measurement__title")
        )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        tariff_service = PriceTariffSettingsFormSet(
            data=request.POST,
            queryset=PriceTariffSettings.objects.filter(tariff=self.object),
            prefix="tariff_service",
        )

        if form.is_valid() and tariff_service.is_valid():
            form.save()
            instances = tariff_service.save(commit=False)
            for instance in instances:
                instance.tariff = self.object
                instance.save()

            for obj in tariff_service.deleted_objects:
                obj.delete()
            return redirect("tariffs")
        else:
            return render(
                request,
                self.template_name,
                self.get_context_data(form=form, tariff_service=tariff_service),
            )


class TariffsSettingsCopyCreateView(CreateView):
    model = TariffsSettings
    template_name = "system_settings/tariff/tariff_settings_add.html"
    success_url = reverse_lazy("tariffs")
    form_class = TariffsSettingsForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        obj_pk = self.request.GET.get("tariff_id")

        if obj_pk:
            obj = get_object_or_404(TariffsSettings, id=obj_pk)
            kwargs["initial"] = {
                "title": obj.title,
                "description": obj.description,
            }
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj_id = self.request.GET.get("tariff_id")
        if obj_id:
            obj = get_object_or_404(TariffsSettings, id=obj_id)
            context["tariff_service"] = PriceTariffSettingsFormSet(
                queryset=PriceTariffSettings.objects.filter(tariff=obj),
                prefix="tariff_service",
            )

        context["services_data_json"] = list(
            ServiceSettings.objects.values("id", "units_measurement__title")
        )
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        tariff_service = PriceTariffSettingsFormSet(
            data=self.request.POST,
            queryset=PriceTariffSettings.objects.none(),
            prefix="tariff_service",
        )
        if form.is_valid() and tariff_service.is_valid():
            new_tariff = form.save()
            instances = tariff_service.save(commit=False)
            for instance in instances:
                instance.pk = None
                instance.tariff = new_tariff
                instance.save()

            for obj in tariff_service.deleted_objects:
                obj.delete()

            return redirect("tariffs")
        else:
            return render(
                request,
                self.template_name,
                {
                    "form": form,
                    "tariff_service": tariff_service,
                    "services_data_json": list(
                        ServiceSettings.objects.values("id", "units_measurement__title")
                    ),
                },
            )


class TariffsSettingsDeleteView(DeleteView):
    template_name = "system_settings/tariff/tariff_settings_table.html"
    model = TariffsSettings
    success_url = reverse_lazy("tariffs")


class PaymentItemsSettingsView(ListView):
    template_name = "system_settings/payment_items/payment_items_table.html"
    model = PaymentItemsSettings


class PaymentItemsSettingsAddView(CreateView):
    template_name = "system_settings/payment_items/payment_items_add.html"
    form_class = PaymentItemsSettingsForm
    success_url = reverse_lazy("payment_items")


class PaymentItemsSettingsUpdateView(UpdateView):
    model = PaymentItemsSettings
    template_name = "system_settings/payment_items/payment_items_edit.html"
    form_class = PaymentItemsSettingsForm
    success_url = reverse_lazy("payment_items")


class PaymentItemsSettingsDeleteView(DeleteView):
    template_name = "system_settings/payment_items/payment_items_table.html"
    model = PaymentItemsSettings
    success_url = reverse_lazy("payment_items")


class ServiceSettingsView(ListView):
    template_name = "system_settings/service_settings.html"
    model = ServiceSettings

    def get_queryset(self):
        return UnitsMeasurement.objects.prefetch_related("service_settings").annotate(
            service_count=Count("service_settings")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_qs = ServiceSettings.objects.select_related("units_measurement").all()

        context["service_settings"] = ServiceSettingsFormSet(
            queryset=service_qs, prefix="service_settings"
        )
        context["units_measurement"] = UnitsMeasurementFormSet(
            queryset=self.get_queryset(), prefix="units_measurement"
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


class RolesView(ListView):
    model = Roles
    template_name = "system_settings/roles.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["roles"] = RolesFormSet(queryset=Roles.objects.all())

        return context

    def post(self, request, *args, **kwargs):
        roles = RolesFormSet(request.POST, queryset=Roles.objects.all())
        if roles.is_valid():
            roles.save()
        return redirect("roles")


class UsersSettingsView(ListView):
    template_name = "system_settings/users/users_settings_table.html"
    model = User

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["filters"] = UsersSettingsFilter()
        return context


class UsersSettingsAddView(CreateView):
    model = User
    template_name = "system_settings/users/users_settings_add.html"
    success_url = reverse_lazy("users")
    form_class = UserSettingsForm


class UsersSettingsDelete(DeleteView):
    model = User
    success_url = reverse_lazy("users")


class UsersSettingsUpdateView(UpdateView):
    model = User
    success_url = reverse_lazy("users")
    template_name = "system_settings/users/users_settings_edit.html"
    form_class = UserSettingsForm
