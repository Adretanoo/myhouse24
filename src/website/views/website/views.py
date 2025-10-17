from django.views.generic import TemplateView

from src.website.models import MainPage


class HomePageView(TemplateView):
    template_name = "website/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["page"] = MainPage.objects.first()
        context["blocks"] = MainPage.objects.all()

        return context
