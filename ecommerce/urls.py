from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from .views import home, about, contact
from addresses.views import checkout_address_create_view,checkout_address_reuse_view
from accounts.views import LoginView, RegisterView,GuestRegisterView
from django.views.generic import TemplateView,RedirectView
from django.contrib.auth.views import LogoutView
from carts.views import cart_detail_api_view
from billing.views import paymend_method_view,paymend_method_create_view
from marketing.views import MarketingPrefenceUpdateView,MailchimpWebhookView
from orders.views import LibraryView
from analytics.views import SalesView,SalesAjaxView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home,name="home"),
    path('about/', about, name="about"),
    # path('accounts/login/', RedirectView.as_view(url="/login")),
    path('accounts/', RedirectView.as_view(url="/account")),
    path('account/', include(('accounts.urls','account'),namespace="account")),
    path('accounts/', include(('accounts.passwords.urls',"password"),namespace='password')),
    path('contact/', contact,name="contact"),
    path('checkout/address/create/', checkout_address_create_view,name="checkout_address_create"),
    path('checkout/address/reuse/', checkout_address_reuse_view, name="checkout_address_reuse"),
    path('analytics/sales/', SalesView.as_view(), name="sales-analytics"),
    path('analytics/sales/data/', SalesAjaxView.as_view(), name="sales-analytics-data"),
    path('bootstrap/', TemplateView.as_view(template_name='bootstrap/example.html')),
    path('login/', LoginView.as_view(),name="login"),
    path('register/guest', GuestRegisterView.as_view(),name="guest_register"),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('library/', LibraryView.as_view(), name='library'),
    path('billing/payment-method/', paymend_method_view, name='billing-payment-method'),
    path('billing/payment-method/create/', paymend_method_create_view, name='billing-payment-method-endpoint'),
    path('cart/', include(('carts.urls', 'carts'), namespace='cart')),
    path('api/cart/', cart_detail_api_view, name='api-cart'),
    path('products/', include(('products.urls', 'products'), namespace='products')),
    path('orders/', include(('orders.urls', 'orders'), namespace='orders')),
    path('search/', include(('search.urls', 'search'), namespace='search')),
    path('settings/', RedirectView.as_view(url="/account")),
    path('settings/email/', MarketingPrefenceUpdateView.as_view(), name='marketing-pref'),
    path('webhooks/mailchimp/', MailchimpWebhookView.as_view(), name='webhooks-mailchimp'),

]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
