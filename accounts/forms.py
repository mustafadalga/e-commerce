from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import EmailActivation,GuestEmail
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib.auth import authenticate, login,get_user_model
from .signals import user_logged_in



User=get_user_model()

class ReactiveEmailForm(forms.Form):
    email=forms.EmailField()

    def clean_email(self):
        email=self.cleaned_data.get("email")
        qs=EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse("register")
            msg = """
                    This email does not exits, would you like to  <a href="{link}">register</> ?
                  """.format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email




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



class UserDetailChangeForm(forms.ModelForm):
    full_name=forms.CharField(label="Name",required=False,widget=forms.TextInput(attrs={'class':"form-control"}))
    class Meta:
        model=User
        fields=['full_name']

# Admin Paneli kullanıcı bilgileri değiştirme
class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('full_name','email', 'password','is_active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]



class GuestForm(forms.ModelForm):
    class Meta:
        model=GuestEmail
        fields=[
            'email'
        ]

    def __init__(self,request,*args,**kwargs):
        self.request=request
        super(GuestForm,self).__init__(*args,**kwargs)

    def save(self, commit=True):
        # Save the provided password in hashed format
        obj = super(GuestForm, self).save(commit=False)
        if commit:
            obj.save()
            request=self.request
            request.session['guest_email_id'] = obj.id
        return obj


class LoginForm(forms.Form):
    email=forms.EmailField(required=False,label="Email")
    password=forms.CharField(required=False,widget=forms.PasswordInput)

    def __init__(self,request,*args,**kwargs):
        self.request=request
        super(LoginForm,self).__init__(*args,**kwargs)

    def clean(self):
        request=self.request # Gönderilen istekleri bilgileri yeniden kullanmak için
        data=self.cleaned_data
        email = data.get('email')
        password = data.get('password')

        qs=User.objects.filter(email=email)
        if qs.exists():

            #user email is registered,check active
            not_active=qs.filter(is_active=False)
            if not_active.exists():
                link=reverse("account:resend-activation")
                reconfirm_msg="""Go to <a href="{resend_link}">resend confirmable email.</a>""".format(resend_link=link)
                confirm_email=EmailActivation.objects.filter(email=email)
                is_confirmable=confirm_email.confirmable().exists()
                if is_confirmable:# Doğrulama doğru gönderilmişse
                    msg1="Please check your email to confirm your account or "+reconfirm_msg.lower()
                    raise forms.ValidationError(mark_safe(msg1))
                email_confirm_exists=EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:# Doğrulama kodu süresi dolmuşsa
                    msg2="Email not confirmed. "+reconfirm_msg
                    raise forms.ValidationError(mark_safe(msg2))

                if not is_confirmable and not email_confirm_exists: # Doğrulama kodu yoksa
                    raise forms.ValidationError("This user is inactive.")

        user = authenticate(request, email=email, password=password)
        if user is None:
            raise forms.ValidationError("Geçersiz giriş bilgileri")
        else:
            login(request, user)
        self.user=user
        return data

    # def form_valid(self, form):
    #     request=self.request
    #     next_ = request.GET.get('next')
    #     next_post = request.POST.get('next')
    #     redirect_path = next_ or next_post or None
    #     email = form.cleaned_data.get('email')
    #     password = form.cleaned_data.get('password')
    #
    #     if user is not None:
    #         if not user.is_active: #  is_active default value = True
    #             messages.error(request,"This user is inactive")
    #             return super(LoginView, self).form_invalid(form)
    #         login(request, user)
    #         user_logged_in.send(user.__class__, instance=user, request=request)
    #         try:
    #             del request.session['guest_email_id']
    #         except:
    #             pass
    #         if is_safe_url(redirect_path, request.get_host()):
    #             return redirect(redirect_path)
    #         else:
    #             return redirect('/')
    #     return super(LoginView,self).form_invalid(form)


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
        user.is_active=False # send confirmation email
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

