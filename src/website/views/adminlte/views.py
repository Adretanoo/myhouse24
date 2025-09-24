from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.website.forms import MainPageForm, SeoForm, MainPageBLockFormSet
from src.website.models import MainPage, MainPageBlock


class MainPageView(TemplateView):
    template_name = "adminlte/main_page/main_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        main_page = MainPage.objects.first()
        seo = main_page.seo if main_page else None

        main_blocks = MainPageBLockFormSet(instance=main_page, prefix="main_blocks")

        context["main_page"] = MainPageForm(instance=main_page)
        context["main_blocks"] = main_blocks
        context["seo"] = SeoForm(instance=seo, prefix="seo")

        return context

    def post(self, request, *args, **kwargs):
        main_page_instance = MainPage.objects.first()
        seo_instance = main_page_instance.seo if main_page_instance else None

        main_blocks = MainPageBLockFormSet(
            request.POST,
            request.FILES,
            prefix="main_blocks",
            instance=main_page_instance,
            queryset=MainPageBlock.objects.filter(main_page=main_page_instance),
        )
        main_page = MainPageForm(
            request.POST, request.FILES, instance=main_page_instance
        )
        seo = SeoForm(request.POST, instance=seo_instance, prefix="seo")

        print("Опис головної сторінки:", request.POST.get("description"))
        print("Опис блоків:", request.POST.getlist("main_blocks-*-description"))
        if main_blocks.is_valid() and main_page.is_valid() and seo.is_valid():
            main_page.save()
            seo.save()
            main_blocks.save()
            return redirect("main_page")

        context = self.get_context_data()
        context["main_page"] = main_page
        context["seo"] = seo
        context["main_blocks"] = main_blocks
        return self.render_to_response(context)
