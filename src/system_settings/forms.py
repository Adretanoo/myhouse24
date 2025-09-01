from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.forms.widgets import TextInput, Textarea, Select
from src.system_settings.models import (
    PaymentDetailsSettings,
    UnitsMeasurement,
    ServiceSettings,
    Roles,
    PaymentItemsSettings,
    TariffsSettings,
    PriceTariffSettings,
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


class PaymentItemsSettingsForm(ModelForm):
    class Meta:
        model = PaymentItemsSettings
        fields = ["title", "translation_type"]
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control",
                    "required": "true",
                }
            ),
            "translation_type": Select(
                attrs={
                    "class": "form-control",
                }
            ),
        }
        labels = {"title": "Название", "translation_type": " Приход/расход "}


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


class TariffsSettingsForm(ModelForm):
    class Meta:
        model = TariffsSettings
        fields = ["title", "description"]
        widgets = {
            "title": TextInput(
                attrs={
                    "class": "form-control",
                    "required": "true",
                }
            ),
            "description": Textarea(
                attrs={
                    "class": "form-control",
                    "required": "true",
                    "rows": "5",
                }
            ),
        }
        labels = {"title": "Название тарифа", "description": "Описание тарифа"}


class PriceTariffSettingsForm(ModelForm):
    class Meta:
        model = PriceTariffSettings
        fields = ["service", "price"]
        widgets = {
            "price": TextInput(
                attrs={
                    "class": "form-control",
                    "required": "true",
                    "value": "0.00",
                }
            ),
            "service": Select(
                attrs={
                    "class": "form-control service-select",
                }
            ),
        }
        labels = {
            "price": "Цена",
            "service": "Услуга",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["service"].label_from_instance = lambda obj: obj.title


PriceTariffSettingsFormSet = modelformset_factory(
    PriceTariffSettings,
    form=PriceTariffSettingsForm,
    extra=0,
    can_delete=True,
)
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
