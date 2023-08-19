from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ReferralCode(models.Model):
    invite_code = models.CharField(max_length=12,
                                   null=False,
                                   blank=False,
                                   verbose_name='Код приглашения')
    host_user = models.ForeignKey(User,
                                  on_delete=models.CASCADE,
                                  verbose_name='Владелец')

    class Meta:
        default_related_name = 'refer_codes'
        verbose_name = 'Реферальный код'
        verbose_name_plural = 'Реферальные коды'

    def __str__(self):
        return self.invite_code
