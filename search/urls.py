from django.urls import path,re_path

from .views import (
SearchProductView
)

urlpatterns = [
    path('', SearchProductView.as_view(),name="query"),
]
