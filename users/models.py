from django.contrib.auth.models import AbstractUser
from django.db import models


class Location(models.Model):
    name = models.CharField(max_length=50, unique=True)
    lat = models.FloatField(null=True)
    lng = models.FloatField(null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Локация"
        verbose_name_plural = "Локации"


class User(AbstractUser):
    ROLE = [
        ("admin", "Администратор"),
        ("moderator", "Модератор"),
        ("member", "Участник")
    ]

    role = models.CharField(max_length=9, choices=ROLE, default="member")
    age = models.PositiveIntegerField(null=True)
    locations = models.ManyToManyField(Location)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
