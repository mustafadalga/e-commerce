from django.shortcuts import render,redirect
from .forms import MarketingPrefenceForm
from .models import MarketingPrefence
from django.views.generic import UpdateView,View
from django.http import HttpResponse
from  django.conf import settings
from django.contrib.messages.views import SuccessMessageMixin
from .mixins import CsrfExemptMixin
from .utils import Mailchimp
MAILCHIP_EMAIL_LIST_ID=getattr(settings,"MAILCHIP_EMAIL_LIST_ID",None)


class MarketingPrefenceUpdateView(SuccessMessageMixin,UpdateView):
    form_class = MarketingPrefenceForm
    template_name = 'marketing/forms.html'
    success_url ='/settings/email/'
    success_message = "E-posta tercihlerini başarıyla güncellendi"

    # Kullanıcı girişi yapılmadığında yönlendir
    def dispatch(self, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            return redirect("/login/?next=/settings/email/")# HttpResponse("Not allowed", status=400)
        return super(MarketingPrefenceUpdateView,self).dispatch(*args,**kwargs)


    def get_context_data(self, **kwargs):
        content=super(MarketingPrefenceUpdateView,self).get_context_data(*kwargs)
        content['title']="Marketing Email Preferences"
        return content


    def get_object(self):
        user = self.request.user
        obj,created=MarketingPrefence.objects.get_or_create(user=user)
        return obj


"""
data[merges][LNAME]:
data[id]: 66d177a222
data[action]: unsub
data[merges][ADDRESS]:
data[email]: fatih@gmail.com
data[merges][BIRTHDAY]:
data[web_id]: 57733545
data[merges][FNAME]:
data[merges][EMAIL]: fatih@gmail.com
data[ip_opt]: 95.2.10.156
fired_at: 2019-10-02 16:30:46
data[list_id]: 3e6f34b9b6
data[reason]: manual
data[email_type]: html
type: unsubscribe
data[merges][PHONE]:
"""

class MailchimpWebhookView(CsrfExemptMixin,View):  # HTTP GET -- def get()
    def get(self,request,*args,**kwargs):
        return HttpResponse("Thank you", status=200)

    def post(self,request,*args,**kwargs):
        data = request.POST
        list_id = data.get("data[id]")
        if str(list_id) == str(MAILCHIP_EMAIL_LIST_ID):
            hook_type = data.get("type")
            email = data.get("data[email]")
            response_status, response = Mailchimp().check_subcription_status(email)
            sub_status = response['status']
            is_subbed = None
            mailchimp_subbed = None
            if sub_status == "subscribed":
                is_subbed, mailchimp_subbed = (True, True)
            elif sub_status == "unsubscribed":
                is_subbed, mailchimp_subbed = (False, False)

            if is_subbed is not None and mailchimp_subbed is not None:
                qs = MarketingPrefence.objects.filter(user__email__iexact=email)
                if qs.exist():
                    qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))

        return HttpResponse("Thank you", status=200)

# def mailchimp_webhook_view(request):
#     data=request.POST
#     list_id=data.get("data[id]")
#     if str(list_id)==str(MAILCHIP_EMAIL_LIST_ID):
#         hook_type = data.get("type")
#         email = data.get("data[email]")
#         response_status,response=Mailchimp().check_subcription_status(email)
#         sub_status=response['status']
#         is_subbed=None
#         mailchimp_subbed=None
#         if sub_status=="subscribed":
#             is_subbed,mailchimp_subbed=(True,True)
#         elif sub_status=="unsubscribed":
#             is_subbed, mailchimp_subbed = (False, False)
#
#
#         if is_subbed is not None and mailchimp_subbed is not None:
#             qs = MarketingPrefence.objects.filter(user__email__iexact=email)
#             if qs.exist():
#                 qs.update(subscribed=is_subbed, mailchimp_subscribed=mailchimp_subbed, mailchimp_msg=str(data))
#
#
#     return HttpResponse("Thank you",status=200)