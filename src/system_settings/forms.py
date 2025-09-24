from django import forms
from django.contrib.auth.password_validation import validate_password
from django.forms import ModelForm
from django.forms.models import modelformset_factory
from django.forms.widgets import TextInput, Textarea, Select, PasswordInput
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


units_choices = list(UnitsMeasurement.objects.values_list("id", "title"))


class ServiceSettingsForm(ModelForm):
    units_measurement = forms.ChoiceField(
        choices=units_choices,
        widget=forms.Select(attrs={"class": "form-control"}),
        label="Ед. изм.",
    )

    class Meta:
        model = ServiceSettings
        fields = ["title", "units_measurement", "is_counters"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
        }
        labels = {
            "title": "Услуга",
            "is_counters": "Показывать в счетчиках",
        }

    def clean_units_measurement(self):
        """перетворюємо id → UnitsMeasurement"""
        unit_id = self.cleaned_data["units_measurement"]
        try:
            return UnitsMeasurement.objects.get(pk=unit_id)
        except UnitsMeasurement.DoesNotExist:
            raise forms.ValidationError("Неверная единица измерения")


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


class UserSettingsForm(ModelForm):
    password = forms.CharField(
        required=False,
        label="Пароль",
        widget=PasswordInput(attrs={"class": "form-control"}),
    )
    confirm_password = forms.CharField(
        required=False,
        label="Повторить пароль",
        widget=PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "status",
            "job_title",
        ]
        widgets = {
            "first_name": TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "email": TextInput(attrs={"class": "form-control", "required": "true"}),
            "last_name": TextInput(attrs={"class": "form-control", "required": "true"}),
            "phone_number": TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "status": Select(attrs={"class": "form-control", "required": "true"}),
            "job_title": Select(attrs={"class": "form-control", "required": "true"}),
        }

        labels = {
            "first_name": "Имя",
            "last_name": "Фамилия",
            "phone_number": "Телефон",
            "job_title": "Роль",
            "status": "Статус",
            "email": "Email (логин)",
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        is_create = self.instance.pk is None

        if is_create:
            if not password:
                self.add_error(
                    "password", "Пароль обязателен при создании пользователя"
                )
            elif password != confirm_password:
                self.add_error("password", "Пароли не совпадают")
            else:
                validate_password(password)

        else:
            if password or confirm_password:
                if password != confirm_password:
                    self.add_error("password", "Пароли не совпадают")
                else:
                    validate_password(password)

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


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
