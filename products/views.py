
from django.views.generic import ListView,DetailView
from django.shortcuts import render,get_object_or_404
from .models import Product
from django.http import Http404
from carts.models import Cart
from analytics.mixins import ObjectViewedMixin

# Create your views here.


class ProductFeaturedListView(ListView):
    template_name = "products/list.html"

    #
    # def get_queryset(self,*args,**kwargs):
    #     request=self.request
    #     return Product.objects.all()

    def get_queryset(self,*args,**kwargs):
        request=self.request
        return Product.objects.all().featured()


class ProductFeaturedDetailView(ObjectViewedMixin,DetailView):
    # template_name = "products/featured-detail.html"
    #
    # def get_queryset(self,*args,**kwargs):
    #     request=self.request
    #     return Product.objects.featured()

    # 2.yol
    # queryset = Product.objects.all()
    # template_name = "products/featured-detail.html"

    # 3.Yol
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context=super(ProductListView,self).get_context_data(**kwargs)
    #     print(context)
    #     return context
    #

    def get_context_data(self,*args, **kwargs):
        context=super(ProductListView,self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)  # Yapılan isteğin sepet bilgileri
        context['cart']=cart_obj   # Sepet Bilgileri
        return context

    # def get_queryset(self,*args,**kwargs):
    #     request=self.request
    #     return Product.objects.all()


#Sadece bu yol kullanılacak
def product_list_view(request):
    queryset = Product.objects.all()
    context={
     'object_list':queryset
    }
    return render(request,"products/list.html",context)


class ProductDetailSlugView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self,*args, **kwargs):
        context=super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)  # Yapılan isteğin sepet bilgileri
        context['cart']=cart_obj   # Sepet Bilgileri
        return context

    # def get_object(self, *args,**kwargs):
    #     request=self.request
    #     slug=self.kwargs.get('slug')
    #
    #     try:
    #         instance=Product.objects.get(slug=slug,active=True)
    #     except Product.DoesNotExist:
    #         raise Http404("Not Found .. ")
    #     except Product.MultipleObjectsReturned:
    #         qs = Product.objects.filter(slug=slug,active=True)
    #         instance=qs.first()
    #     except Http404:
    #         raise Http404("HTTP 404 HATASI")
    #     return instance


class ProductDetailView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"


    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(ProductDetailView,self).get_context_data(**kwargs)
        print(context)
        context['abc']=123
        return context

    def get_object(self, *args,**kwargs):
        request=self.request
        pk=self.kwargs.get('pk')

        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Ürün bulunamadı CLASS")
        return instance


    # def get_queryset(self,*args,**kwargs):
    #     request=self.request
    #     pk = self.kwargs.get('pk')
    #     return Product.objects.filter(pk=pk)

#Sadece bu yol kullanılacak
def product_detail_view(request,pk=None,*args,**kwargs):
    # object=Product.objects.get(pk=pk)

    # Yol 1
    # instance=get_object_or_404(Product,pk=pk)


    #Yol 2
    # try:
    #     instance=Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     raise Http404("Ürün bulunamadı!")
    # except:
    #     pass

    # YOl 3
    instance=Product.objects.get_by_id(pk)
    if instance is None:
        raise Http404("Ürün bulunamadı")
    # print(instance)

    # YOL 4
    # qs=Product.objects.filter(id=pk)
    # if qs.exists() and qs.count()==1:
    #     instance=qs.first()
    # else:
    #     raise Http404("Ürün bulunamadı 2")

    context={
     'object':instance,
    }
    return render(request,"products/detail.html",context)

