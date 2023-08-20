from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class UserProfile(models.Model):
    owner = models.OneToOneField(User,
                                 on_delete=models.CASCADE,
                                 verbose_name='Пользователь')
    phone_number = models.CharField(max_length=12,
                                    unique=True,
                                    null=False,
                                    blank=False,
                                    verbose_name='Номер телефона')
    referral_code = models.CharField(max_length=6,
                                     null=False,
                                     blank=False,
                                     unique=True,
                                     verbose_name='Реферальный код')
    invite_code = models.CharField(max_length=6,
                                   null=True,
                                   blank=True,
                                   unique=False,
                                   verbose_name='Код приглашения')

    class Meta:
        default_related_name = 'profile'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return self.phone_number
