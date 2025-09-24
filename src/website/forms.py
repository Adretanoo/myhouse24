from django import forms
from django.forms.models import inlineformset_factory
from src.website.models import Seo, MainPage, MainPageBlock


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


MainPageBLockFormSet = inlineformset_factory(
    MainPage, MainPageBlock, form=MainPageBlockForm, extra=6, can_delete=False
)
