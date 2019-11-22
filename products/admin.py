from django.contrib import admin

# Register your models here.
from .models import Product,ProductFile


class ProductFileInline(admin.TabularInline):# Product file class'ını Product ile birleştirir.
    model = ProductFile
    extra = 1 # Default dosya sayısı 1

class ProductAdmin(admin.ModelAdmin):
    list_display = ['__str__','slug']
    inlines = [ProductFileInline]
    class Meta:
        model=Product

admin.site.register(Product,ProductAdmin)