from django.urls import reverse
from ajax_datatable.views import AjaxDatatableView
from src.system_settings.models import (
    PaymentItemsSettings,
    TranslationType,
    TariffsSettings,
)


class PaymentItemsAjaxDatatableView(AjaxDatatableView):
    model = PaymentItemsSettings

    column_defs = [
        {
            "name": "title",
            "title": "Название",
            "visible": True,
            "orderable": True,
            "searchable": False,
        },
        {
            "name": "translation_type",
            "title": "Приход/расход",
            "visible": True,
            "orderable": True,
            "searchable": False,
        },
        {
            "name": "actions",
            "visible": True,
            "title": "",
            "placeholder": True,
            "searchable": False,
            "orderable": False,
            "width": 20,
        },
    ]

    initial_order = [[0, "asc"]]

    def get_initial_queryset(self, request=None):
        return self.model.objects.all()

    def customize_row(self, row, obj):
        if obj.translation_type == TranslationType.INCOME:
            row["translation_type"] = (
                f'<span class="text text-green">{obj.get_translation_type_display()}</span>'
            )
        elif obj.translation_type == TranslationType.EXPENSE:
            row["translation_type"] = (
                f'<span class="text text-red">{obj.get_translation_type_display()}</span>'
            )
        else:
            row["translation_type"] = obj.get_translation_type_display()
        edit_url = reverse("payment_items_edit", kwargs={"pk": obj.pk})
        delete_url = reverse("payment_items_delete", kwargs={"pk": obj.pk})
        row["actions"] = f"""
            <div class="btn-group pull-right">
                <a class="btn btn-default btn-sm" href="{edit_url}" title="Редактировать" data-toggle="tooltip">
                    <i class="fa fa-pencil-alt"></i>
                </a>
               <button type="button" class="btn btn-default btn-sm delete-button"
                    title="Удалить"
                    data-url="{delete_url}"
                    data-id="{obj.pk}"
                    data-toggle="tooltip"
                    data-confirm="Вы уверены, что хотите удалить этот элемент?">
                    <i class="fa fa-trash"></i>
               </button>
            </div>
        """
        return row


class TariffsSettingsAjaxView(AjaxDatatableView):
    model = TariffsSettings
    column_defs = [
        {
            "name": "title",
            "title": "Название тарифа",
            "visible": True,
            "searchable": False,
        },
        {
            "name": "description",
            "title": "Описание тарифа",
            "visible": True,
            "searchable": False,
        },
        {
            "name": "edit_date",
            "title": "Дата редактирования",
            "visible": True,
            "searchable": False,
        },
        {"name": "actions", "title": "", "visible": True, "searchable": False},
    ]

    def customize_row(self, row, obj):
        row["edit_date"] = f"{obj.edit_date:%d.%m.%Y - %H:%M}" if obj.edit_date else ""
        edit_url = reverse("tariffs_edit", kwargs={"pk": obj.pk})
        delete_url = reverse("tariffs_delete", kwargs={"pk": obj.pk})
        copy_url = f"{reverse('tariffs_copy')}?tariff_id={obj.pk}"
        row["actions"] = f"""
            <div class="btn-group pull-right">
            <a class="btn btn-default btn-sm" href="{copy_url}" title="Копировать" data-toggle="tooltip">
                <i class="fa fa-clone"></i>
            </a>
                <a class="btn btn-default btn-sm" href="{edit_url}" title="Редактировать" data-toggle="tooltip">
                    <i class="fa fa-pencil-alt"></i>
                </a>
               <button type="button" class="btn btn-default btn-sm delete-button"
                    title="Удалить"
                    data-url="{delete_url}"
                    data-id="{obj.pk}"
                    data-toggle="tooltip"
                    data-confirm="Вы уверены, что хотите удалить этот элемент?">
                    <i class="fa fa-trash"></i>
               </button>
            </div>
        """
        return row

    def get_initial_queryset(self, request=None):
        return self.model.objects.all()
