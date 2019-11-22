from django.contrib import admin

from .models import MarketingPrefence


class MarketingPrefenceAdmin(admin.ModelAdmin):
    list_display = ['__str__','subscribed','updated']

    readonly_fields = ['mailchimp_msg','mailchimp_subscribed','timestamp','updated']
    class   Meta:
        model=MarketingPrefence
        fields=[
            'user',
            'subscribed',
            'mailchimp_msg',
            'mailchimp_subscribed',
            'timestamp',
            'updated'
        ]


admin.site.register(MarketingPrefence,MarketingPrefenceAdmin)

