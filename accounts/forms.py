from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField


User=get_user_model()

   # Admin Paneli kullanıcı oluşturma
class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name','email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

# Admin Paneli kullanıcı bilgileri değiştirme
class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class GuestForm(forms.Form):
    email=forms.EmailField()


class LoginForm(forms.Form):
    email=forms.EmailField(required=False,label="Email")
    password=forms.CharField(required=False,widget=forms.PasswordInput)



class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('full_name','email',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parolalar Eşleşmiyor")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active=False # send confirmation email

        if commit:
            user.save()
        return user


#
# class RegisterForm(forms.Form):
#     username=forms.CharField(required=False)
#     email=forms.EmailField()
#     password=forms.CharField(required=False,widget=forms.PasswordInput)
#     password2=forms.CharField(label="Confirm password",required=False,widget=forms.PasswordInput)
#
#
#     def clean_username(self):
#         username=self.cleaned_data.get('username')
#         qs=User.objects.filter(username=username)
#         if qs.exists():
#             raise forms.ValidationError("Böyle bir kullanıcı zaten mevcut")
#         return username
#
#     def clean_email(self):
#         email=self.cleaned_data.get('email')
#         qs=User.objects.filter(email=email)
#         if qs.exists():
#             raise forms.ValidationError("Böyle bir email adresi zaten mevcut")
#         return email
#
#     def clean(self):
#         data=self.cleaned_data
#         password=self.cleaned_data.get('password')
#         password2=self.cleaned_data.get('password2')
#         if password!=password2:
#             raise forms.ValidationError("Parolalar eşleşmiyor!")
#         return data

