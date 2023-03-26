from employee.models import User
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(label='password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_number',)

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the employee, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = '__all__'


class UserAdmin(BaseUserAdmin):
    # The forms to add and change employee instances
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('user_number',)
    inlines = []
    list_filter = ()
    ordering = ()
    fieldsets = (
        (None, {
            'fields':
                (
                    'user_number', 'is_active', 'password'
                )
        }),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields':
                (
                    'user_number', 'password', 'is_active',
                ),
        }),
    )


# User
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('user_number', 'role', 'is_superuser', 'is_admin', 'password')

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(User, UserAdmin)
