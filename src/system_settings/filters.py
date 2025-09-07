from django import forms
from django.forms import TextInput, Select

from src.system_settings.models import JobTitle
from src.users.models import Status


class UsersSettingsFilter(forms.Form):
    name = forms.CharField(
        required=False,
        widget=TextInput(attrs={"class": "form-control", "id": "filter_name"}),
    )
    email = forms.CharField(
        required=False,
        widget=TextInput(attrs={"class": "form-control", "id": "filter_email"}),
    )
    phone_number = forms.CharField(
        required=False,
        widget=TextInput(attrs={"class": "form-control", "id": "filter_phone"}),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[("", "")] + list(Status.choices),
        widget=Select(attrs={"class": "form-control", "id": "filter_status"}),
    )
    job_title = forms.ChoiceField(
        required=False,
        choices=[("", "")] + list(JobTitle.choices),
        widget=Select(attrs={"class": "form-control", "id": "filter_job_title"}),
    )
