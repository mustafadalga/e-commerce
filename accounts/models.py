from django.db import models
from datetime import timedelta
from django.contrib.auth.models import (
AbstractBaseUser,BaseUserManager
)
from django.db.models.signals import pre_save,post_save
from django.conf import settings
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import get_template
from ecommerce.utils import unique_key_generator
from django.utils import timezone
from django.db.models import Q


# DEFAULT_ACTIVATION_DAYS=getattr(settings,"DEFAULT_ACTIVATION_DAYS",7)
DEFAULT_ACTIVATION_DAYS=7

class UserManager(BaseUserManager):
    def create_user(self,email,full_name=None,password=None,is_active=True,is_staff=True,is_admin=True):
        if not email:
            raise ValueError("Kullanıcıların bir e-posta adresi olmalı!")
        if not password:
            raise ValueError("Kullanıcıların bir parolası bulunmalı!")
        # if not full_name:
        #     raise ValueError("Kullanıcıların Tam adı olmalı!")
        user_obj=self.model(
            email=self.normalize_email(email),
            full_name=full_name
        )
        user_obj.set_password(password) #change user password
        user_obj.is_active=is_active
        user_obj.admin=is_admin
        user_obj.staff=is_staff
        user_obj.save(using=self.db)
        return user_obj

     # Normal kullanıcı oluşturma
    def create_staffuser(self,email,full_name=None,password=None):
        user=self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True
        )
        return user

    # Admin oluşturma
    def create_superuser(self,email,full_name=None,password=None):
        user=self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_admin=True,
            is_staff=True
        )
        return user


class User(AbstractBaseUser):
    email=models.EmailField(unique=True,max_length=255)
    full_name=models.CharField(max_length=255,blank=True,null=True)
    # active=models.BooleanField(default=True)
    is_active=models.BooleanField(default=True)
    staff=models.BooleanField(default=False) # staff user non superuser
    admin=models.BooleanField(default=False) # superuser
    timestamp=models.DateTimeField(auto_now_add=True)
    # confirm=models.BooleanField(default=False)
    # confirmed_date=models.DateTimeField(default=False)

    USERNAME_FIELD='email' #Username

    #email an password required
    REQUIRED_FIELDS =[]

    objects=UserManager()

    def __str__(self):
        return str(self.email)

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email

    # Model izinleri
    def has_perm(self,perm,obj=None):
        return True

    # Model izinleri
    def has_module_perms(self,app_label):
        return  True

    @property
    def is_staff(self):
        if self.is_admin:
            return True
        return self.staff



    @property
    def is_admin(self):
        return self.admin

    # Varsayılan olarak http://127.0.0.1:8000/register/ kayıt olunan kullanıcılar için active=False olarak belirlenmiştir.
    # active=False olan kullanıcılar kayıtlı olsa bile kullanıcı girişi yapamaz.(http://127.0.0.1:8000/login/)
    # Aktif pasif özelliğini aşağıdaki metot sağlar.

    # @property
    # def is_active(self):
    #     return self.active

class EmailActivationManagerQuerySet(models.query.QuerySet): # EmailActivation.objects.all().confirmable()

    # Aktivasyon kodu geçerlilik süresini kontrol etme
    def confirmable(self):
        now=timezone.now()
        # does my object have a timestamp in here
        start_range=now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range=now

        return self.filter(
            activated=False,
            forced_expired=False,

        ).filter(
            timestamp__gt=start_range,
            timestamp__lte=end_range
        )
        # gt:daha büyük
    """
      ('gt', 'Büyüktür'),
     ('gte', 'Büyük veya eşit'),
     ('lte', 'Daha küçük veya ona eşit'),
    ('exact', 'Is equal to'),
    ('not_exact', 'Is not equal to'),
    ('lt', 'Lesser than'),
    ('gt', 'Greater than'),
    ('gte', 'Greater than or equal to'),
    ('lte', 'Lesser than or equal to'),
    ('startswith', 'Starts with'),
    ('endswith', 'Ends with'),
    ('contains', 'Contains'),
    ('not_contains', 'Does not contain'),


    """

class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationManagerQuerySet(self.model,using=self._db)

    def confirmable(self):
        return self.get_queryset().confirmable()

    def email_exists(self,email):
        return self.get_queryset().filter(
            Q(email=email) |
            Q(user__email=email)
            ).filter(activated=False)


class EmailActivation(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    email=models.EmailField()
    key=models.CharField(max_length=120,blank=True,null=True)
    activated=models.BooleanField(default=False)
    forced_expired=models.BooleanField(default=False)# Sona erdi mi
    expires=models.IntegerField(default=7)#Son erme süresi 7 gün
    timestamp=models.DateTimeField(auto_now_add=True)
    update=models.DateTimeField(auto_now_add=True)

    objects=EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs=EmailActivation.objects.filter(pk=self.pk).confirmable()
        if qs.exists():
            return True
        return False

    def activate(self):
        if self.can_activate():
            user=self.user
            # pre activation user signal
            user.is_active=True
            user.save()
            # post activation signal for user
            self.activated=True
            self.save()
            return True
        return False

    def regenerate(self):
        self.key=None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url=getattr(settings,'BASE_URL','https://django-eticaret.herokuapp.com/')
                key_path=reverse("account:email-activate",kwargs={'key':self.key})
                path="{base}{path}".format(base=base_url,path=key_path)
                context={
                    "path":path,
                    "email":self.email
                }

                txt_=get_template("registration/emails/verify.txt").render(context)
                html_=get_template("registration/emails/verify.html").render(context)
                subject="1-Click Email Verification"
                from_email=settings.DEFAULT_FROM_EMAIL
                recipient_list=[self.email]

                sendMail=send_mail(
                    subject=subject,
                    message=txt_,
                    from_email=from_email,
                    recipient_list=recipient_list,
                    html_message=html_,
                    fail_silently=False
                )
            return sendMail
        return False


def pre_save_email_activation(sender,instance,*args,**kwargs):
    print("****")
    print("1")
    print("****")
    if not instance.activated and not instance.forced_expired:
        print("2")
        if not instance.key:
            print("3")
            instance.key=unique_key_generator(instance)

pre_save.connect(pre_save_email_activation,sender=EmailActivation)

def post_save_user_create_receiver(sender,instance,created,*args,**kwargs):
    print("****")
    print("4")
    print("****")
    if created:
        obj=EmailActivation.objects.create(user=instance,email=instance.email)
        print("5")
        obj.send_activation()

post_save.connect(post_save_user_create_receiver,sender=User)
"""
 1 Kullanıcı hesabı oluşturulduğunda doğrulama maili gönder
 2 
"""


# Create your models here.
class GuestEmail(models.Model):
    email=models.EmailField()
    active=models.BooleanField(default=True)
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.email