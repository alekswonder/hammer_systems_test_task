from django.contrib import admin

from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('pk', 'owner', 'phone_number',
                    'referral_code', 'invite_code')
    list_editable = ('phone_number',)
    search_fields = ('owner', 'phone_number')
    empty_value_display = 'пусто'


admin.site.register(UserProfile, UserProfileAdmin)
