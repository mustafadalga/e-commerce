from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Cart
from orders.models import Order
from products.models import Product
from accounts.forms import LoginForm, GuestForm
from billing.models import BillingProfile
from addresses.forms import AddressForm
from addresses.models import Address

from django.conf import settings
import stripe
STRIPE_SECRET_KEY=getattr(settings,'STRIPE_SECRET_KEY',"sk_test_53qdSBhMf6DpdVhkomQzAkSD00t9IcQotu") # Secret key
STRIPE_PUB_KEY=getattr(settings,'STRIPE_PUB_KEY',"pk_test_5wkb1M4U4Z0WN44BcoH2XnXJ00pa2DsSqv") # #Publishable key
stripe.api_key=STRIPE_SECRET_KEY


def cart_detail_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    # products = [{"name": x.name, "price": x.price} for x in cart_obj.products.all()]
    products_list = []
    for x in cart_obj.products.all():
        products_list.append(
            {
                'id':x.id,
                "name": x.title,
                "price": x.price,
                "url":x.get_absolute_url()
            }
        )
    cart_data = {"products": products_list, "subtotal": cart_obj.subtotal, "total": cart_obj.total}
    return JsonResponse(cart_data)


def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    return render(request, 'carts/home.html', {'cart': cart_obj})


def cart_update(request):
    product_id = request.POST.get('product_id')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)  # Urun id'i getirildi
        except Product.DoesNotExists:
            print("Show message to user , product is gone?")
            return redirect("cart:home")
        cart_obj, new_obj = Cart.objects.new_or_get(request)  # Sepet getirildi
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            added = False
        else:
            cart_obj.products.add(product_obj)  # Sepete ürün eklendi
            added = True

        # Navbar sepetteki ürün sayısını göstermek için
        request.session["cart_items"] = cart_obj.products.count()
        # return redirect(product_obj.get_absolute_url()) #Ürünün sayfasına yönlendirildi.

        if request.is_ajax():
            print("Ajax İsteği")
            json_data = {
                'added': added,
                'removed': not added,
                'cartItemCount': cart_obj.products.count()
            }
            return JsonResponse(json_data,status=200)
            # return JsonResponse({"message":"Error 404"},status_code=404)
    return redirect('cart:home')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_or_get(request)  # Sepet getirildi
    # print("Sepet:")
    # print(cart_obj)
    # print(cart_created)
    # print("******************")
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart:home')
    login_form = LoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get('billing_address_id', None)
    shipping_address_id = request.session.get('shipping_address_id', None)

    # Fatura Profili oluşturma oluşturmak için,manuel olarak oluşturulan bir metot billing->models.py>BillingProfileManager
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card=False

    if billing_profile is not None:
        # Kayıtlı adresleri kullanabilmek için kullanıcı girişi yapılması gerekmekte
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session['shipping_address_id']
        if billing_address_id:
            order_obj.billing_address_id = Address.objects.get(id=billing_address_id)
            del request.session['billing_address_id']
        if billing_address_id or shipping_address_id:
            order_obj.save()
        has_card=billing_profile.has_card
        # print("**********Billing********")
        # print(billing_profile)
        # # print(billing_profile.email)
        # print("***********")

    # Check that order is done
    # Odeme işlemi tamamlandı mı ?
    if request.method == "POST":
        is_prepared = order_obj.check_done()
        if is_prepared:
            did_charge,crg_msg=billing_profile.charge(order_obj)
            if did_charge:
                order_obj.mark_paid()
                request.session['cart_items'] = 0
                del request.session['cart_id']
                if not billing_profile.user:
                    billing_profile.set_cards_inactive() # Misafir kullanıcı ise kart bilgileri bir sonraki sefer için tutulmaz
                return redirect("cart:success")
            else:
                print(crg_msg)
                print("selam")
                return redirect("cart:checkout")

    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'login_form': login_form,
        'guest_form': guest_form,
        'address_form': address_form,
        'address_qs': address_qs,
        'has_card':has_card,
        'publish_key':STRIPE_PUB_KEY,
    }
    return render(request, 'carts/checkout.html', context)

    """
    misafir kullanıcı olarak giriş yaptığında
    -sipariş misafir email olarak oluşturuldu ve true
    -fatura profili misafir email olarak oluşturuldu
    
    İlk misafir girişi yapıldığında
    ->misafir email fatura profili oluşturulur
    ->Sipariş oluşturulur.
    
    ->Sipariş emaili:misafir email
    ->Sepet kullanıcı :Null
    ->Sipariş active:True
    
    ******************
    Kullanıcı giriş yapıldığında
    
    ->sepet requeste ait olup aktive olan tüm siparişler false yapılır.(misafir kullanıcı emailine göre sorgulama yapılmaz)
    ->Yeni bir sipariş oluşturulur.
    ->sepet kullanıcı adı,giriş yapan kullanıcı adı olarak değişir.
    ->
    
    """


def checkout_done(request):
    return render(request, 'carts/checkout-done.html')
