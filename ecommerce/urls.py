from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .views import home, about, contact
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
from accounts.views import LoginView, RegisterView,guest_register_view
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from carts.views import cart_detail_api_view
from billing.views import paymend_method_view,paymend_method_create_view
from marketing.views import MarketingPrefenceUpdateView,MailchimpWebhookView

# from products.views import (
#     ProductListView,
#     product_list_view,
#     product_detail_view,
#     ProductDetailView,
#     ProductFeaturedListView,
#     ProductFeaturedDetailView,
#     ProductDetailSlugView,
# )

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="home"),
    path('about/', about, name="about"),
    path('contact/', contact,name="contact"),
    path('checkout/address/create/', checkout_address_create_view,name="checkout_address_create"),
    path('checkout/address/reuse/', checkout_address_reuse_view, name="checkout_address_reuse"),
    path('bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html')),
    path('login/', LoginView.as_view(),name="login"),
    path('register/guest', guest_register_view,name="guest_register"),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('billing/payment-method/', paymend_method_view, name='billing-payment-method'),
    path('billing/payment-method/create/', paymend_method_create_view, name='billing-payment-method-endpoint'),
    path('cart/', include(('carts.urls', 'carts'), namespace='cart')),
    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('search/', include(('search.urls', 'search'), namespace='search')),
    path('settings/email/', MarketingPrefenceUpdateView.as_view(), name='marketing-pref'),
    path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),

    # path('account/', include(('social_django.urls', 'social_django'), namespace='social')),


    # path('featured/', ProductFeaturedListView.as_view()),
    # path('featured/<int:pk>/', ProductFeaturedDetailView.as_view()),
    # path('products/', ProductListView.as_view()),
    # path('products2/', product_list_view),
    # # path('products/<int:pk>/', ProductDetailView.as_view()),
    # re_path(r'^products/(?P<slug>[\w-]+)/$', ProductDetailSlugView.as_view()),
    # path('products2/<int:pk>/', product_detail_view),


]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
