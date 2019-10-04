from django.db import models
from django.contrib.auth.models import (
AbstractBaseUser,BaseUserManager
)

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
        user_obj.active=is_active
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
    active=models.BooleanField(default=True)
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
        return self.email

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
        return self.staff



    @property
    def is_admin(self):
        return self.admin

    # Varsayılan olarak http://127.0.0.1:8000/register/ kayıt olunan kullanıcılar için active=False olarak belirlenmiştir.
    # active=False olan kullanıcılar kayıtlı olsa bile kullanıcı girişi yapamaz.(http://127.0.0.1:8000/login/)
    # Aktif pasif özelliğini aşağıdaki metot sağlar.

    @property
    def is_active(self):
        return self.active


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)


# Create your models here.
class GuestEmail(models.Model):
    email=models.EmailField()
    active=models.BooleanField(default=True)
    update=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)



    def __str__(self):
        return self.email