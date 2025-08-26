from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import *


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'phone_number', 'designation',)}),
        (_('Permissions'), {
            'fields': ('is_staff', 'groups', "user_permissions",),
        }),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    readonly_fields = ('email',)


admin.site.register(User, CustomUserAdmin)
