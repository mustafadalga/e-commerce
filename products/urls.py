from django.urls import path,re_path

from .views import (
    ProductListView,
    # product_list_view,
    product_detail_view,
    ProductDetailView,
    # ProductFeaturedListView,
    # ProductFeaturedDetailView,
    ProductDetailSlugView,
)

urlpatterns = [
    # path('featured/', ProductFeaturedListView.as_view()),
    # path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
    path('', ProductListView.as_view(),name="list"),
    # path('products2/', product_list_view),
    # path('products/<int:pk>/', ProductDetailView.as_view()),
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(),name="detail"),
    # path('products2/<int:pk>/', product_detail_view),
]
