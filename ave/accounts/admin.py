from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username',
                     'email',
                    'is_staff', 'is_active',
                     'last_login']
    fieldsets = (
        (None, {'fields': (
                           'username', 'email', 'full_name',
                           'is_staff', 'is_active',
                           'groups',  'password', 'user_type', 'user_permissions')}),
    )
admin.site.register(User, CustomUserAdmin)
