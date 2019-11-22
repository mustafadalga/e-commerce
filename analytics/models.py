from django.conf import settings
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sessions.models import Session
from .signals import object_viewed_signal
from django.db.models.signals import pre_save,post_save
from accounts.signals import user_logged_in
from .utils import get_client_ip

User=settings.AUTH_USER_MODEL

FORCE_SESSION_TO_ONE=getattr(settings,'FORCE_SESSION_TO_ONE',False)
FORCE_INACTIVE_USER_ENDSESSION=getattr(settings,'FORCE_INACTIVE_USER_ENDSESSION',False)


class ObjectViewedQuerySet(models.query.QuerySet):
    def by_model(self,model_class,model_queryset=False):
        c_type = ContentType.objects.get_for_model(model_class)  # model instance.__class__
        qs = self.filter(content_type=c_type)
        if model_queryset:
            views_ids=[x.object_id for x in qs]
            return model_class.objects.filter(pk__in=views_ids)
        return qs

class ObjectViewedManager(models.Manager):
    def get_queryset(self):
        return ObjectViewedQuerySet(self.model,using=self._db)

    def by_model(self,model_class,model_queryset=False):
        return self.get_queryset().by_model(model_class,model_queryset)



class ObjectViewed(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE) # User instance,instance.id
    ip_address=models.CharField(max_length=220,blank=True,null=True)
    content_type=models.ForeignKey(ContentType,on_delete=models.CASCADE) # User,Product,Order,Cart,Adress herhangi bir model olabilir. Tüm django modelleri select olarak listelenir.
    object_id=models.PositiveIntegerField()  # User id,product id,order id
    content_object=GenericForeignKey('content_type','object_id') # Product instance
    timestamp=models.DateTimeField(auto_now_add=True)

    objects=ObjectViewedManager()


    # X kullanıcı şu saat şunu görüntüledi
    #content_type :Görüntülenen modeller
    #object_id:görüntülenen modelin içerisindeki verilerin id'si    (content_type)Product modelinde,id'si(object_id) 5 olan ürün görüntülendi

    def __str__(self):
        return "%s viewed on %s" % (self.content_object,self.timestamp)

    class Meta:
        ordering=['-timestamp']  # most recent saved show up first
        verbose_name='Object viewed'
        verbose_name_plural="Objects viewed"


def object_viewed_receiver(sender,instance,request,*args,**kwargs):
    # print("***********************")
    c_type=ContentType.objects.get_for_model(sender) # model instance.__class__
    # print(sender)
    # print(instance)
    # print(request)
    # print(request.user)
    user=None
    if request.user.is_authenticated:
        user=request.user
    new_view_obj=ObjectViewed.objects.create(
        user=user,
        content_type=c_type,
        object_id=instance.id,
        ip_address=get_client_ip(request),
    )

object_viewed_signal.connect(object_viewed_receiver)




class UserSession(models.Model):
    user=models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE) # User instance,instance.id
    ip_address=models.CharField(max_length=220,blank=True,null=True)
    session_key=models.CharField(max_length=100,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    active=models.BooleanField(default=True)
    ended=models.BooleanField(default=False)


    def __str__(self):
        return self.user

   # Kullanıcı session silme
    def end_session(self):
        session_key=self.session_key
        ended=self.ended
        try:
            Session.objects.get(pk=session_key).delete()
            self.active=False
            self.ended=True
            self.save()
        except:
            pass
        return self.ended





#kullanıcı giriş yaptığında, diğer tüm oturumlarını kapatma
def post_save_session_receiver(sender,instance,created,*args,**kwargs):
    print("Oturum kapatma")
    if created:
        # Aynı kullanıcnın diğer oturumlarını kapatma
        print("Diğer Oturum kapatma")
        qs=UserSession.objects.filter(user=instance.user,ended=False,active=True).exclude(id=instance.id)
        for i in qs:
            i.end_session()
    if not instance.active and not instance.ended:
        instance.end_session()

if FORCE_SESSION_TO_ONE:
    post_save.connect(post_save_session_receiver,sender=UserSession)

def post_save_user_changed_receiver(sender,instance,created,*args,**kwargs):
    if not created:
        print("post_save_user_changed_receiver")
        if instance.is_active==False:
            print("post_save_user_changed_receiver 2 ")
            qs = UserSession.objects.filter(user=instance.user, ended=False, active=True).exclude(id=instance.id)
            for i in qs:
                i.end_session()


if FORCE_INACTIVE_USER_ENDSESSION:
    post_save.connect(post_save_user_changed_receiver,sender=User)



# Kullanıcı giriş yaptığında kullanıcı bilgilerini kaydetme
def user_logged_in_receiver(sender,instance,request,*args,**kwargs):
    print(instance)
    print("Kullanıcı Girişi")
    user=instance
    ip_address=get_client_ip(request)
    session_key=request.session.session_key
    UserSession.objects.create(
        user=user,
        ip_address=ip_address,
        session_key=session_key
    )

user_logged_in.connect(user_logged_in_receiver)