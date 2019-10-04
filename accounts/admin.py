from django.contrib import admin
from django.contrib.auth import get_user_model
from .forms import UserAdminChangeForm,UserAdminCreationForm
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.
from .models import GuestEmail

User=get_user_model()

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'admin')
    list_filter = ('admin','staff','active')
    fieldsets = (
        (None, {'fields': ('full_name','email', 'password')}),
        # ('Personal info', {'fields': ('full_name',)}),
        ('Permissions', {'fields': ('admin','staff','active')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}
        ),
    )
    search_fields = ('email','full_name',)
    ordering = ('email',)
    filter_horizontal = ()


class GuestEmailAdmin(admin.ModelAdmin):
    search_fields = ['email']
    class Meta:
        model=GuestEmail


admin.site.register(User,UserAdmin)
admin.site.register(GuestEmail,GuestEmailAdmin)

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)