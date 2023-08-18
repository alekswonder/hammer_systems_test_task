from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'phone_number', 'invite_code', 'referral_code',)
    list_editable = ('phone_number', )
    search_fields = ('phone_number', )
    list_filter = ('phone_number', 'referral_code')
    empty_value_display = 'пусто'


admin.site.register(CustomUser, CustomUserAdmin)
