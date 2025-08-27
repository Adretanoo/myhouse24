from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.forms.widgets import TextInput, Textarea, Select
from src.system_settings.models import (
    PaymentDetailsSettings,
    UnitsMeasurement,
    ServiceSettings,
    Roles,
)


class PaymentDetailsForm(ModelForm):
    class Meta:
        model = PaymentDetailsSettings
        fields = ["title", "information"]
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Мой дом",
                    "type": "text",
                }
            ),
            "information": Textarea(
                attrs={
                    "class": "form-control",
                    "rows": "5",
                    "placeholder": "Информация",
                }
            ),
        }
        labels = {"title": "Название компании", "information": "Информация"}


class RolesForm(ModelForm):
    class Meta:
        model = Roles
        fields = "__all__"
        exclude = ["job_title"]


class UnitsMeasurementForm(ModelForm):
    class Meta:
        model = UnitsMeasurement
        fields = ["title"]
        widgets = {
            "title": TextInput(attrs={"class": "form-control", "required": "true"})
        }
        labels = {"title": "Ед. изм."}


class ServiceSettingsForm(ModelForm):
    class Meta:
        model = ServiceSettings
        fields = ["title", "units_measurement", "is_counters"]
        widgets = {
            "title": TextInput(attrs={"class": "form-control", "required": "true"}),
            "units_measurement": Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }
        labels = {
            "title": "Услуга",
            "is_counters": "Показывать в счетчиках",
            "units_measurement": "Ед. изм.",
        }


RolesFormSet = modelformset_factory(
    Roles,
    form=RolesForm,
    extra=0,
    can_delete=False,
)
UnitsMeasurementFormSet = modelformset_factory(
    UnitsMeasurement,
    form=UnitsMeasurementForm,
    extra=0,
    can_delete=True,
)
ServiceSettingsFormSet = modelformset_factory(
    ServiceSettings,
    form=ServiceSettingsForm,
    extra=0,
    can_delete=True,
)
