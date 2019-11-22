from django.urls import path,re_path

from .views import (
    ProductListView,
    ProductDetailSlugView,
    ProductDownloadView,
)

urlpatterns = [
    path('', ProductListView.as_view(),name="list"),
    re_path(r'^(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view(),name="detail"),
    re_path(r'^(?P<slug>[\w-]+)/(?P<pk>\d+)$', ProductDownloadView.as_view(),name="download"),
]
