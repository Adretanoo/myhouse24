from django.urls import reverse_lazy
from django.views.generic import UpdateView

from src.system_settings.forms import PaymentDetailsForm
from src.system_settings.models import PaymentDetailsSettings


class PaymentDetailsView(UpdateView):
    template_name = "system_settings/payment_details.html"
    form_class = PaymentDetailsForm
    success_url = reverse_lazy("payment_details")

    def get_object(self, queryset=None):
        return PaymentDetailsSettings.objects.first()
