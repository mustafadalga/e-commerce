from django.db import models
from django.db.models import Q
from ecommerce.utils import unique_slug_generator,get_filename
from django.db.models.signals import pre_save
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from ecommerce.aws.utils import ProtectedS3BotoStorage
from  ecommerce.aws.download.utils import AWSDownload
import os


class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True, active=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query) |
                Q(tag__title__icontains=query)  # Tag models'i title sutunu Tags>models.py Tag'dan gelir.
        )
        return self.filter(lookups).distinct()


class ProductManager(models.Manager):

    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    # Sadece aktif olanların içerisinden işlem yap.
    def all(self):
        return self.get_queryset().active()

    def featured(self):  # Produt.objects.featured()
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self, query):
        return self.get_queryset().active().search(query)


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=10, default=39.99)
    image = models.ImageField(upload_to='products/%Y-%m-%d/', null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_digital = models.BooleanField(default=False) # User Library

    objects = ProductManager()

    def get_absolute_url(self):
        # return "/products/{slug}/".format(slug=self.slug)
        return reverse("products:detail", kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    @property
    def name(self):
        return self.title


    def get_downloads(self):
        qs=self.productfile_set.all()
        return qs



def product_pre_save_receive(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receive, sender=Product)


def upload_product_file_loc(instance,filename):
    slug=instance.product.slug
    id_=instance.id
    if id_ is None:
        Klass = instance.__class__
        qs = Klass.objects.order_by("-pk")
        if qs.exists():
            id_ = qs.first().id + 1
        else:
            id_=0
    if not slug:
        slug = unique_slug_generator(instance.product)
    location="products/{slug}/{id}/".format(slug=slug,id=id_)
    return location+filename # path/to/filename.txt




class ProductFile(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    name=models.CharField(max_length=120,null=True,blank=True)
    file=models.FileField(upload_to=upload_product_file_loc,storage=ProtectedS3BotoStorage())#FileSystemStorage(location=settings.PROTECTED_ROOT))# Özel dosya yükleme konumu oluşturma
    # filepath=models.TextField() # /protected/path/to/the/file
    free=models.BooleanField(default=False)   # purchase required
    user_required=models.BooleanField(default=False) # user doesn't matter


    def __str__(self):
        return str(self.file.name)

    def get_default_url(self):
        return self.product.get_absolute_url()

    @property
    def display_name(self):
        og_name= get_filename(self.file.name)
        if self.name:
            return self.name
        return og_name

    def generate_download_url(self):
        bucket =getattr(settings,"AWS_STORAGE_BUCKET_NAME")
        region =getattr(settings,"S3DIRECT_REGION")
        access_key =getattr(settings,"AWS_ACCESS_KEY_ID")
        secret_key =getattr(settings,"AWS_SECRET_ACCESS_KEY")
        if not secret_key or not access_key or not bucket or not region:
            return "/product-not-found/"

        PROTECTED_DIR_NAME=getattr(settings,"PROTECTED_DIR_NAME","protected")
        path = "{base}/{file_path}".format(base=PROTECTED_DIR_NAME,file_path=str(self.file))
        aws_dl_object = AWSDownload(access_key, secret_key, bucket, region)
        file_url = aws_dl_object.generate_url(path=path, new_filename=self.display_name)
        return file_url

    def get_download_url(self):
        return reverse("products:download",kwargs={"slug":self.product.slug,"pk":self.pk})


