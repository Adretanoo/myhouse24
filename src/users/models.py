from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from src.system_settings.models import JobTitle


class Status(models.TextChoices):
    NEW = "new", "Новый"
    ACTIVE = "active", "Активен"
    INACTIVE = "inactive", "Отключен"


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    patronymic = models.CharField(max_length=120)
    birthday = models.DateField(blank=True, null=True)
    description = models.TextField()
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r"^\+?1?\d{9,15}$",
                message="Телефон должен быть в формате: +380XXXXXXXXX",
            )
        ],
    )
    viber = models.CharField(max_length=32)
    telegram = models.CharField(max_length=32)
    status = models.CharField(choices=Status.choices, max_length=32, default=Status.NEW)
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    job_title = models.CharField(
        choices=JobTitle.choices, max_length=32, default=JobTitle.DIRECTOR
    )
    user_number = models.IntegerField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
