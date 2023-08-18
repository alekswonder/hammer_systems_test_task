from django.contrib import admin

from .models import ReferralCode


class ReferralCodeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'referral_code', 'host_user')
    empty_value_display = 'пусто'


admin.site.register(ReferralCode, ReferralCodeAdmin)
