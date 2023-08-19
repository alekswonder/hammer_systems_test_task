from django.contrib.auth.models import AbstractUser
from django.db import models

from .managers import CustomUserManager


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=12,
                                    unique=True,
                                    null=False,
                                    blank=False,
                                    verbose_name='Номер телефона',)
    referral_code = models.CharField(max_length=6,
                                     null=False,
                                     blank=False,
                                     unique=True,
                                     verbose_name='Реферальный код')
    invite_code = models.CharField(max_length=6,
                                   null=True,
                                   blank=True,
                                   verbose_name='Код приглашения')

    USERNAME_FIELD = 'phone_number'

    objects = CustomUserManager()

    class Meta:
        default_related_name = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username
