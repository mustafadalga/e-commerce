from django.db import models
from django.db.models import Q
from ecommerce.utils import unique_slug_generator
from django.db.models.signals import pre_save
from django.urls import reverse


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True,active=True)

    def active(self):
        return self.filter(active=True)

    def search(self,query):
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query) |
                Q(tag__title__icontains=query)# Tag models'i title sutunu Tags>models.py Tag'dan gelir.
        )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    # Sadece aktif olanların içerisinden işlem yap.
    def all(self):
        return self.get_queryset().active()

    def featured(self): #Produt.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self,query):
        return self.get_queryset().active().search(query)



# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    slug=models.SlugField(blank=True,unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=39.99)
    image = models.ImageField(upload_to='products/%Y-%m-%d/', null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()


    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail",kwargs={'slug':self.slug})


    def __str__(self):
        return self.title

def product_pre_save_receive(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)


pre_save.connect(product_pre_save_receive,sender=Product)