from django.db import models
from django.conf import settings
from django.db.models.signals import post_save,pre_save

from .utils import Mailchimp

# Create your models here.

class MarketingPrefence(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    subscribed=models.BooleanField(default=True)
    mailchimp_subscribed=models.NullBooleanField(blank=True)
    mailchimp_msg=models.TextField(null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.email


def marketing_pref_create_receiver(sender,instance,created,*args,**kwargs):
    if created:
       # status_code,response_data=Mailchimp().subscribe(instance.user.email)
       status_code,response_data=Mailchimp().add_email(instance.user.email)
       # print(response_data)

# Üye olan kullanıcıların Pazarlama üyeliği oluşturulduğu an,aynı zamanda mailchimp listesine de ekle
post_save.connect(marketing_pref_create_receiver,sender=MarketingPrefence)



def marketing_pref_update_receiver(sender,instance,*args,**kwargs):
    if instance.subscribed!=instance.mailchimp_subscribed:#veritabanı ile mailchimpteki abonelik durumu farklıysa
        if instance.subscribed: # Abone ise
            status_code, response_data = Mailchimp().subscribe(instance.user.email)
        else:
            status_code, response_data = Mailchimp().unsubscribe(instance.user.email)

        if response_data['status']=="subscribed": # Mailchimp'teki abonelik durumuna göre veritabanı abonelik durumunu değiştir.
            instance.subscribed = True
            instance.mailchimp_subscribed=True
            instance.mailchimp_msg=response_data
        else:
            instance.subscribed = False
            instance.mailchimp_subscribed = False
            instance.mailchimp_msg = response_data

# Veritabanı ile mailchimpteki abonelik durumlarını senkronizasyonunu sağlama
pre_save.connect(marketing_pref_update_receiver, sender=MarketingPrefence)


"""
1-Kullanıcı üyeliği oluştur
2-pazarlama üyeliği oluştur
3-pazarlama üyeliği oluşturulan kullanıcıyı mailchimp listesine ekle
"""

# kullanıcılar üyelik oluşturulduğunda aynı zamanda pazarlama üyeliği de oluştur.
def make_marketing_pref_receiver(sender,instance,created,*args,**kwargs):
    """
    User model
    """
    if created:
        MarketingPrefence.objects.get_or_create(user=instance)

# kullanıcılar üyelik oluşturulduğunda aynı zamanda pazarlama üyeliği de oluştur.
post_save.connect(make_marketing_pref_receiver,sender=settings.AUTH_USER_MODEL)