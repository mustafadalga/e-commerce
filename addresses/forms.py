from django import forms
from .models import Address


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            'adress_line_1',
            'adress_line_2',
            'city',
            'country',
            'state',
            'postal_code',
        ]
