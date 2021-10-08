from django.contrib import admin
from user.models import Account
from django.contrib.auth.admin import UserAdmin
from django.forms import Textarea
from django.db import models

from rest_framework_simplejwt.token_blacklist import models as token_models
from rest_framework_simplejwt.token_blacklist.admin import OutstandingTokenAdmin


class UserAdminConfig(UserAdmin):
    model = Account
    search_fields = ('email', 'last_name', 'first_name',)
    list_filter = ('email', 'last_name', 'first_name', 'is_active', 'is_staff')
    ordering = ('-register_date',)
    list_display = ('email', 'last_name', 'first_name',
                    'is_active', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'last_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff')}
         ),
    )


class NewOutstandingTokenAdmin(OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True  # or whatever logic you want


admin.site.unregister(token_models.OutstandingToken)
admin.site.register(token_models.OutstandingToken,
                    NewOutstandingTokenAdmin)

admin.site.register(Account, UserAdminConfig)
