from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from django.utils.http import is_safe_url
from django.conf import settings

from .models import BillingProfile,Card

import stripe
STRIPE_SECRET_KEY=getattr(settings,'STRIPE_SECRET_KEY',"sk_test_53qdSBhMf6DpdVhkomQzAkSD00t9IcQotu") # Secret key
STRIPE_PUB_KEY=getattr(settings,'STRIPE_PUB_KEY',"pk_test_5wkb1M4U4Z0WN44BcoH2XnXJ00pa2DsSqv") # #Publishable key
stripe.api_key=STRIPE_SECRET_KEY


# http://127.0.0.1:8000/billing/payment-method/?next=/billing/    Add Payment Method
def paymend_method_view(request):
    # if request.user.is_authenticated:
    #     billing_profile=request.user.billingprofile
    #     my_customer_id=billing_profile.customer_id
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)

    if not billing_profile:
        return redirect("/cart")

    next_url=None
    next_=request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url=next_
    return render(request,"billing/payment-method.html",{'publish_key':STRIPE_PUB_KEY,'next_url':next_url})


def paymend_method_create_view(request):
    if request.method=="POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message":"Bu kullanıcı bulunamadı"}, status=401)



        # Kart bilgilerini alma ve kaydetme(stripe.com)
        print(request.POST)
        token=request.POST.get("token")
        if token is not None:
            new_card_obj=Card.objects.add_new(billing_profile,token)
            print(new_card_obj)


        return JsonResponse({'message':"Success! Your card was added."})
    return HttpResponse("error",status=401)
