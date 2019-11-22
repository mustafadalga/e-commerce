from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UserAdminChangeForm,UserAdminCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import GuestEmail,EmailActivation

User=get_user_model()

class UserAdmin(BaseUserAdmin):
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm


    list_display = ('email', 'admin')
    list_filter = ('admin','staff')
    fieldsets = (
        (None, {'fields': ('full_name','email', 'password','is_active')}),
        # ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin','staff')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','full_name',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User,UserAdmin)
admin.site.unregister(Group)

class EmailActivationAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model=EmailActivation


admin.site.register(EmailActivation,EmailActivationAdmin)

class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model=GuestEmail


admin.site.register(GuestEmail,GuestEmailAdmin)
