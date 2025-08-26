from django.forms import ModelForm
from django.forms.widgets import TextInput, Textarea
from src.system_settings.models import PaymentDetailsSettings


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
