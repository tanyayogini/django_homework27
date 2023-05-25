from django.contrib.auth.models import AbstractUser
from django.db import models

from users.validators import check_birth, check_domains


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
    birth_date = models.DateField(null=True, validators=[check_birth])
    email = models.EmailField(validators=[check_domains])

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
