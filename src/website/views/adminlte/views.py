from django.shortcuts import redirect
from django.views.generic import TemplateView

from src.website.forms import (
    MainPageForm,
    SeoForm,
    MainPageBLockFormSet,
    AboutUsPageForm,
    AboutUsPageGalleryFormSet,
    AboutUsPageDocumentsFormSet,
    ContactsPageForm,
    ServiceCardFormSet,
    TariffsCardFormSet,
    TariffsPageForm,
    AboutUsPageAdditionalGalleryFormSet,
)
from src.website.models import (
    MainPage,
    MainPageBlock,
    AboutUsPage,
    ContactsPage,
    ServicePage,
    TariffsPage,
)


class MainPageView(TemplateView):
    template_name = "adminlte/main_page.html"

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


class AboutUsPageView(TemplateView):
    template_name = "adminlte/about_page.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        about_page = AboutUsPage.objects.first()
        seo = about_page.seo if about_page else None

        about_page_gallery = AboutUsPageGalleryFormSet(
            instance=about_page, prefix="about_page_gallery"
        )
        about_page_additional_gallery = AboutUsPageAdditionalGalleryFormSet(
            instance=about_page, prefix="about_page_additional_gallery"
        )
        about_page_documents = AboutUsPageDocumentsFormSet(
            instance=about_page, prefix="about_page_documents"
        )

        context["about"] = AboutUsPageForm(instance=about_page)
        context["about_gallery"] = about_page_gallery
        context["about_additional_gallery"] = about_page_additional_gallery
        context["about_documents"] = about_page_documents
        context["seo"] = SeoForm(instance=seo, prefix="seo")

        return context

    def post(self, request, *args, **kwargs):
        about_page_instance = AboutUsPage.objects.first()

        about_form = AboutUsPageForm(
            request.POST, request.FILES, instance=about_page_instance
        )
        seo_form = SeoForm(
            request.POST,
            prefix="seo",
            instance=about_page_instance.seo if about_page_instance else None,
        )

        about_gallery_formset = AboutUsPageGalleryFormSet(
            request.POST,
            request.FILES,
            instance=about_page_instance,
            prefix="about_page_gallery",
        )
        about_additional_gallery_formset = AboutUsPageAdditionalGalleryFormSet(
            request.POST,
            request.FILES,
            instance=about_page_instance,
            prefix="about_page_additional_gallery",
        )
        about_documents_formset = AboutUsPageDocumentsFormSet(
            request.POST,
            request.FILES,
            instance=about_page_instance,
            prefix="about_page_documents",
        )

        forms_valid = (
            about_form.is_valid()
            and seo_form.is_valid()
            and about_gallery_formset.is_valid()
            and about_additional_gallery_formset.is_valid()
            and about_documents_formset.is_valid()
        )

        if forms_valid:
            about_page = about_form.save(commit=False)
            seo = seo_form.save()
            about_page.seo = seo
            about_page.save()

            about_gallery_formset.instance = about_page
            about_gallery_formset.save()

            about_additional_gallery_formset.instance = about_page
            about_additional_gallery_formset.save()

            about_documents_formset.instance = about_page
            about_documents_formset.save()

            return redirect("about_page")

        context = self.get_context_data()
        context["about"] = about_form
        context["seo"] = seo_form
        context["about_gallery"] = about_gallery_formset
        context["about_additional_gallery"] = about_additional_gallery_formset
        context["about_documents"] = about_documents_formset

        return self.render_to_response(context)


class ServicePageView(TemplateView):
    template_name = "adminlte/service_page.html"
    model = ServicePage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service_page = ServicePage.objects.first()
        seo = service_page.seo if service_page else None
        service_cards = ServiceCardFormSet(instance=service_page, prefix="service_card")

        context["service_cards"] = service_cards
        context["seo"] = SeoForm(instance=seo, prefix="seo")
        return context

    def post(self, request, *args, **kwargs):
        service_page_instance = ServicePage.objects.first()
        if not service_page_instance:
            service_page_instance = ServicePage.objects.create()

        seo_instance = service_page_instance.seo if service_page_instance else None
        service_cards = ServiceCardFormSet(
            request.POST,
            request.FILES,
            instance=service_page_instance,
            prefix="service_card",
        )
        seo = SeoForm(request.POST, instance=seo_instance, prefix="seo")

        if service_cards.is_valid() and seo.is_valid():
            service_cards.save()
            for form in service_cards.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            seo.save()

            return redirect("services_page")

        context = self.get_context_data()
        context["service_cards"] = service_cards
        context["seo"] = seo
        return self.render_to_response(context)


class TariffsPageView(TemplateView):
    template_name = "adminlte/tariffs_page.html"
    model = TariffsPage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        tariff_page_obj = TariffsPage.objects.first()
        tariff_page = TariffsPageForm(instance=tariff_page_obj, prefix="tariffs_page")

        seo = tariff_page_obj.seo if tariff_page_obj else None
        tariff_cards = TariffsCardFormSet(
            instance=tariff_page_obj, prefix="tariffs_card"
        )

        context["tariff_page"] = tariff_page
        context["tariff_cards"] = tariff_cards
        context["seo"] = SeoForm(instance=seo, prefix="seo")
        return context

    def post(self, request, *args, **kwargs):
        tariff_page_instance = TariffsPage.objects.first()
        tariff_page = TariffsPageForm(
            request.POST, prefix="tariffs_page", instance=tariff_page_instance
        )
        seo_instance = tariff_page_instance.seo if tariff_page_instance else None
        tariff_cards = TariffsCardFormSet(
            request.POST,
            request.FILES,
            instance=tariff_page_instance,
            prefix="tariffs_card",
        )
        seo = SeoForm(request.POST, instance=seo_instance, prefix="seo")

        if tariff_page.is_valid() and tariff_cards.is_valid() and seo.is_valid():
            tariff_page.save()

            for form in tariff_cards.deleted_forms:
                if form.instance.pk:
                    form.instance.delete()

            tariff_cards.save()
            seo.save()
            return redirect("tariffs_page")

        context = self.get_context_data()
        context["tariff_page"] = tariff_page
        context["tariff_cards"] = tariff_cards
        context["seo"] = seo
        return self.render_to_response(context)


class ContactsPageView(TemplateView):
    template_name = "adminlte/contacts_page.html"
    model = ContactsPage

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contacts_page = ContactsPage.objects.first()
        seo = contacts_page.seo if contacts_page else None

        context["contacts"] = ContactsPageForm(instance=contacts_page)
        context["seo"] = SeoForm(instance=seo, prefix="seo")

        return context

    def post(self, request, *args, **kwargs):
        contacts_page_instance = ContactsPage.objects.first()
        seo_instance = contacts_page_instance.seo if contacts_page_instance else None
        contacts_page = ContactsPageForm(request.POST, instance=contacts_page_instance)
        seo = SeoForm(request.POST, instance=seo_instance, prefix="seo")

        if contacts_page.is_valid() and seo.is_valid():
            contacts_page.save()
            seo.save()
            return redirect("contacts_page")

        context = self.get_context_data()
        context["contacts"] = contacts_page
        context["seo"] = seo
        return self.render_to_response(context)
