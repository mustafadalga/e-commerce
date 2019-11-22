from products.models import Product
from django.views.generic import ListView

class SearchProductView(ListView):
    template_name = "search/view.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context=super(SearchProductView,self).get_context_data(**kwargs)
        query=self.request.GET.get('q')
        context['query']=query
        return context

    def get_queryset(self,*args,**kwargs):
        request=self.request
        method_dict=request.GET
        query=method_dict.get('q',None)
        if query is not None:
            return Product.objects.search(query)
        return Product.objects.featured()