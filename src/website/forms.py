from django import forms
from django.core.validators import RegexValidator
from django.forms.models import inlineformset_factory
from src.website.models import (
    Seo,
    MainPage,
    MainPageBlock,
    AboutUsPage,
    AboutUsPageGallery,
    AboutUsPageAdditionalGallery,
    AboutUsPageDocuments,
    ContactsPage,
    ServiceCard,
    ServicePage,
    TariffsPage,
    TariffsCard,
)

phone_validator = RegexValidator(
    regex=r"^\+?1?\d{9,15}$", message="Формат +380 00 000 0000"
)


class SeoForm(forms.ModelForm):
    class Meta:
        model = Seo
        fields = ["title", "description", "keywords"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": "6"}),
            "keywords": forms.Textarea(attrs={"class": "form-control", "rows": "6"}),
        }
        labels = {
            "title": "Title",
            "description": "Description",
            "keywords": "Keywords",
        }


class MainPageForm(forms.ModelForm):
    class Meta:
        model = MainPage
        fields = [
            "title",
            "description",
            "slide1",
            "slide2",
            "slide3",
            "is_url_application",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "slide1": forms.FileInput(attrs={"accept": "image/*"}),
            "slide2": forms.FileInput(attrs={"accept": "image/*"}),
            "slide3": forms.FileInput(attrs={"accept": "image/*"}),
            "description": forms.Textarea(
                attrs={"class": "wysihtml5 form-control", "id": "description-toolbar"}
            ),
        }
        labels = {
            "title": "Заголовок",
            "description": "Краткий текст",
            "slide1": "Рекомендуемый размер: (1920x800)",
            "slide2": "Рекомендуемый размер: (1920x800)",
            "slide3": "Рекомендуемый размер: (1920x800)",
            "is_url_application": "Показать ссылки на приложения",
        }


class MainPageBlockForm(forms.ModelForm):
    class Meta:
        model = MainPageBlock
        fields = ["title", "description", "main_image"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "wysihtml5 form-control",
                    "rows": "6",
                    "required": "true",
                }
            ),
            "main_image": forms.FileInput(attrs={"accept": "image/*"}),
        }
        labels = {
            "title": "Заголовок блока",
            "description": "Описание",
            "main_image": "Рекомендуемый размер: (1000x600)",
        }


class AboutUsPageForm(forms.ModelForm):
    class Meta:
        model = AboutUsPage
        fields = [
            "title",
            "description",
            "additional_title",
            "additional_description",
            "photo_director",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "description": forms.Textarea(
                attrs={"class": "wysihtml5 form-control", "rows": "6"}
            ),
            "additional_title": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "additional_description": forms.Textarea(
                attrs={"class": "wysihtml5 form-control", "rows": "6"}
            ),
            "photo_director": forms.FileInput(attrs={"accept": "image/*"}),
        }
        labels = {
            "title": "Заголовок",
            "description": "Краткий текст",
            "additional_title": "Заголовок",
            "additional_description": "Краткий текст",
            "photo_director": "Рекомендуемый размер: (250x310)",
        }


class AboutUsPageGalleryForm(forms.ModelForm):
    class Meta:
        model = AboutUsPageGallery
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }


class AboutUsPageAdditionalGalleryForm(forms.ModelForm):
    class Meta:
        model = AboutUsPageAdditionalGallery
        fields = ["image"]
        widgets = {
            "image": forms.FileInput(attrs={"accept": "image/*"}),
        }


class AboutUsPageDocumentsForm(forms.ModelForm):
    class Meta:
        model = AboutUsPageDocuments
        fields = ["title", "file"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "file": forms.FileInput(attrs={"accept": "document_file/*"}),
        }
        labels = {
            "title": "Название документа",
            "file": "PDF, JPG (макс. размер 20 Mb)",
        }


class ServiceCardForm(forms.ModelForm):
    class Meta:
        model = ServiceCard
        fields = ["title", "description", "main_image"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "wysihtml5 form-control",
                    "rows": "6",
                    "required": "true",
                }
            ),
            "main_image": forms.FileInput(
                attrs={"accept": "image/*", "class": "form-control"}
            ),
        }
        labels = {
            "title": "Название услуги",
            "description": "Описание услуги",
            "main_image": "Рекомендуемый размер: (650x300)",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.instance and self.instance.pk and self.instance.main_image):
            self.fields["main_image"].widget.attrs["required"] = "true"


class TariffsPageForm(forms.ModelForm):
    class Meta:
        model = TariffsPage
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "wysihtml5 form-control",
                    "rows": "6",
                    "required": "true",
                }
            ),
        }

        labels = {
            "title": "Заголовок",
            "description": "Краткий текст",
        }


class TariffsCardForm(forms.ModelForm):
    class Meta:
        model = TariffsCard
        fields = ["signature", "main_image"]
        widgets = {
            "signature": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "main_image": forms.FileInput(
                attrs={"accept": "image/*", "class": "form-control"}
            ),
        }
        labels = {"signature": "Подпись", "main_image": "Файл"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not (self.instance and self.instance.pk and self.instance.main_image):
            self.fields["main_image"].widget.attrs["required"] = "true"


class ContactsPageForm(forms.ModelForm):
    link_site = forms.URLField(
        widget=forms.URLInput(attrs={"class": "form-control", "required": "true"}),
        label="Ссылка на коммерческий сайт",
    )
    phone = forms.CharField(
        validators=[phone_validator],
        widget=forms.TextInput(attrs={"class": "form-control", "required": "true"}),
        label="Телефон",
    )

    class Meta:
        model = ContactsPage
        fields = [
            "title",
            "description",
            "link_site",
            "map",
            "fio",
            "location",
            "address",
            "phone",
            "email",
        ]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "description": forms.Textarea(
                attrs={"class": "wysihtml5 form-control", "rows": "6"}
            ),
            "map": forms.Textarea(attrs={"class": "form-control", "rows": "6"}),
            "fio": forms.TextInput(attrs={"class": "form-control", "required": "true"}),
            "location": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "address": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "required": "true"}
            ),
            "email": forms.EmailInput(
                attrs={"class": "form-control", "required": "true"}
            ),
        }
        labels = {
            "title": "Заголовок",
            "description": "Краткий текст",
            "map": "Код карты",
            "fio": "ФИО",
            "location": "Локация",
            "address": "Адрес",
            "email": "E-mail",
        }


MainPageBLockFormSet = inlineformset_factory(
    MainPage, MainPageBlock, form=MainPageBlockForm, extra=6, can_delete=False
)
AboutUsPageGalleryFormSet = inlineformset_factory(
    AboutUsPage,
    AboutUsPageGallery,
    form=AboutUsPageGalleryForm,
    extra=1,
    can_delete=True,
)
AboutUsPageAdditionalGalleryFormSet = inlineformset_factory(
    AboutUsPage,
    AboutUsPageAdditionalGallery,
    extra=1,
    form=AboutUsPageAdditionalGalleryForm,
    can_delete=True,
)
AboutUsPageDocumentsFormSet = inlineformset_factory(
    AboutUsPage,
    AboutUsPageDocuments,
    extra=0,
    form=AboutUsPageDocumentsForm,
    can_delete=True,
)
ServiceCardFormSet = inlineformset_factory(
    ServicePage, ServiceCard, form=ServiceCardForm, extra=0, can_delete=True
)
TariffsCardFormSet = inlineformset_factory(
    TariffsPage, TariffsCard, form=TariffsCardForm, extra=0, can_delete=True
)
