from django.db import models


class TranslationType(models.TextChoices):
    INCOME = "income", "Приход"
    EXPENSE = "expense", "Расход"


class JobTitle(models.TextChoices):
    DIRECTOR = "director", "Директор"
    MANAGER = "manager", "Управляющий"
    ACCOUNTANT = "accountant", "Бухгалтер"
    ELECTRICIAN = "electrician", "Электрик"
    PLUMBER = "plumber", "Сантехник"


class UnitsMeasurement(models.Model):
    title = models.CharField(max_length=30)

    class Meta:
        db_table = "units_measurement"

    def __str__(self):
        return self.title


class ServiceSettings(models.Model):
    title = models.CharField(max_length=255)
    units_measurement = models.ForeignKey(
        UnitsMeasurement,
        on_delete=models.CASCADE,
        default=1,
        related_name="service_settings",
    )
    is_counters = models.BooleanField(default=False)

    class Meta:
        db_table = "service_settings"


class TariffsSettings(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    edit_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tariffs_settings"
        ordering = ("-id",)


class PriceTariffSettings(models.Model):
    service = models.ForeignKey(ServiceSettings, on_delete=models.CASCADE, default=1)
    tariff = models.ForeignKey(TariffsSettings, on_delete=models.CASCADE)
    price = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        db_table = "price_tariff_settings"


class PaymentDetailsSettings(models.Model):
    title = models.CharField(max_length=255)
    information = models.TextField()

    class Meta:
        db_table = "payment_details_settings"


class PaymentItemsSettings(models.Model):
    title = models.CharField(max_length=255)
    translation_type = models.CharField(
        choices=TranslationType.choices, max_length=10, default=TranslationType.INCOME
    )

    class Meta:
        db_table = "payment_items_settings"


class Roles(models.Model):
    has_statistics = models.BooleanField(default=False)
    has_cash_desk = models.BooleanField(default=False)
    has_receipt = models.BooleanField(default=False)
    has_personal_accounts = models.BooleanField(default=False)
    has_apartments = models.BooleanField(default=False)
    has_owner = models.BooleanField(default=False)
    has_houses = models.BooleanField(default=False)
    has_message = models.BooleanField(default=False)
    has_request = models.BooleanField(default=False)
    has_counters = models.BooleanField(default=False)
    has_site_management = models.BooleanField(default=False)
    has_services = models.BooleanField(default=False)
    has_tariffs = models.BooleanField(default=False)
    has_job_title = models.BooleanField(default=False)
    has_users = models.BooleanField(default=False)
    has_payment_details = models.BooleanField(default=False)
    job_title = models.CharField(choices=JobTitle.choices, max_length=20)

    class Meta:
        db_table = "roles"
