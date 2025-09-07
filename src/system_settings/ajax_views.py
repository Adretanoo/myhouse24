from django.db.models import Q
from django.http import JsonResponse
from django.urls import reverse, reverse_lazy
from ajax_datatable.views import AjaxDatatableView

from src.system_settings.filters import UsersSettingsFilter
from src.system_settings.models import (
    PaymentItemsSettings,
    TranslationType,
    TariffsSettings,
    JobTitle,
)
from src.users.models import User, Status


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


def users_system_settings_data(request):
    qs = User.objects.all()
    filter_form = UsersSettingsFilter(request.GET)

    if filter_form.is_valid():
        if filter_form.cleaned_data.get("name"):
            qs = qs.filter(
                Q(first_name__icontains=filter_form.cleaned_data["name"])
                | Q(last_name__icontains=filter_form.cleaned_data["name"])
            )
        if filter_form.cleaned_data.get("email"):
            qs = qs.filter(email__icontains=filter_form.cleaned_data["email"])
        if filter_form.cleaned_data.get("phone_number"):
            qs = qs.filter(
                phone_number__icontains=filter_form.cleaned_data["phone_number"]
            )
        if filter_form.cleaned_data.get("status"):
            qs = qs.filter(status=filter_form.cleaned_data["status"])
        if filter_form.cleaned_data.get("job_title"):
            qs = qs.filter(job_title__icontains=filter_form.cleaned_data["job_title"])

    data = []
    for u in qs:
        edit_url = reverse_lazy("users_edit", kwargs={"pk": u.pk})
        delete_url = reverse_lazy("users_delete", kwargs={"pk": u.pk})
        send_url = "#"

        data.append(
            {
                "id": u.pk,
                "full_name": f"{u.first_name} {u.last_name}",
                "job_title": JobTitle(u.job_title).label,
                "phone_number": u.phone_number,
                "email": u.email,
                "status": f'<span class="status-label"  data-value={u.status}>{Status(u.status).label}</span>',
                "actions": f"""
                    <div class="btn-group pull-right">
                        <a class="btn btn-default btn-sm" href="{send_url}" title="Отправить приглашение">
                            <i class="fa fa-redo"></i>
                        </a>
                        <a class="btn btn-default btn-sm" href="{edit_url}" title="Редактировать">
                            <i class="fa fa-pencil-alt"></i>
                        </a>
                        <button type="button" class="btn btn-default btn-sm delete-button"
                            data-url="{delete_url}" data-id="{u.pk}" data-confirm="Вы уверены?">
                            <i class="fa fa-trash"></i>
                        </button>
                    </div>
                """,
            }
        )

    return JsonResponse({"data": data})
