from django import forms
from django.contrib.auth import get_user_model

User=get_user_model()

class ContactForm(forms.Form):
    fullname=forms.CharField(required=False,widget=forms.TextInput(
        attrs={
            'class':"form-control",
            'placeholder':'Your Full Name',
        }))
    email=forms.EmailField(required=False,widget=forms.EmailInput(
        attrs={
            'class':'form-control',
            'placeholder': 'Your Email',
        }
    ))
    content=forms.CharField(required=False,widget=forms.Textarea(
        attrs={
            'class':'form-control mb-3',
            'placeholder':'Your Message',
        }))


    def clean_email(self):
        email=self.cleaned_data.get('email')
        if not "gmail.com"  in email:
            raise forms.ValidationError("Email has to be gmail.com")
        return email

    # def clean_content(self):
    #     raise forms.ValidationError("Content is wrong.")

# class LoginForm(forms.Form):
#     username=forms.CharField(required=False)
#     password=forms.CharField(required=False,widget=forms.PasswordInput)

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
#
