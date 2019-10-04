from django import forms
from .models import MarketingPrefence


class MarketingPrefenceForm(forms.ModelForm):
    subscribed=forms.BooleanField(label="Receive Marketing Email",required=None)
    class Meta:
        model=MarketingPrefence
        fields=[
            'subscribed',
        ]