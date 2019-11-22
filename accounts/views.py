from django.contrib.auth import authenticate, login,get_user_model
from django.shortcuts import redirect,render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.views.generic import CreateView,FormView,DetailView,View,UpdateView
from django.views.generic.edit import FormMixin
from .forms import LoginForm,RegisterForm,GuestForm,ReactiveEmailForm,UserDetailChangeForm
from django.utils.http import is_safe_url
from ecommerce.mixins import NextUrlMixin,RequestFormAttachMixin

from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import GuestEmail,EmailActivation
from .signals import user_logged_in


# Yöntem 1
# @login_required   # /accounts/login/?next=/some/path/
# def account_home_view(request):
#     return render(request,"accounts/home.html")

# Yöntem 2 ,
class AccountHomeView(LoginRequiredMixin,DetailView):
    template_name = "accounts/home.html"
    def get_object(self):
        return self.request.user


class AccountEmailActivateView(FormMixin,View):
    success_url = "/login/"
    form_class = ReactiveEmailForm
    key=None
    def get(self,request,key=None,*args,**kwargs):
        self.key=key
        if key is not None:
            qs=EmailActivation.objects.filter(key__iexact=key)
            confirmable_qs=qs.confirmable()
            if confirmable_qs.exists()==1:
                obj=confirmable_qs.first()
                obj.activate()
                messages.success(request,"Your email has been corfirmed.Please login.")
                return redirect('login')
            else:
                activate_qs=qs.filter(activated=True)
                if activate_qs.exists():
                    reset_link=reverse("accounts:password_reset")
                    msg="""
                    Your email has already been confirmed.
                     Do you need to <a href="{link}"> reset your password</a>?
                    """"".format(link=reset_link)
                    messages.success(request,mark_safe(msg))
                    return redirect("login")
        context={"form":self.get_form(),'key':key}
        return render(request,"registration/activation-error.html",context)

    def post(self, request, *args, **kwargs):
        # create form to receive an email
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid(self, form):
        # Here, we would record the user's interest using the message
        # passed in form.cleaned_data['message']
        msg = "Activation link send , please check your email."
        request=self.request
        messages.success(request,msg)
        email=form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user=obj.user
        new_activation=EmailActivation.objects.create(user=user,email=email)
        new_activation.send_activation()

        return super(AccountEmailActivateView,self).form_valid(form)

    def form_invalid(self, form):

        context = {"form": self.get_form(),'key':self.key}
        return render(self.request, "registration/activation-error.html", context)



class GuestRegisterView(NextUrlMixin,RequestFormAttachMixin,CreateView):
    form_class = GuestForm
    default_next = "/register/"

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)

    # def form_valid(self, form):
    #     request=self.request
    #     email = form.cleaned_data.get('email')
    #     new_guest_email = GuestEmail.objects.create(email=email)
    #     return redirect(self.get_next_url())


class LoginView(NextUrlMixin,RequestFormAttachMixin,FormView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    success_url = "/"
    default_next = "/"

    def form_valid(self, form):
        next_path=self.get_next_url()
        return redirect(next_path)



#      #/cart/chechout.html adresinden gelir
#     # /cart/checkout/ ,fatura profili görüntülendiğinde giriş yapmayan kullanıcılar için giriş yaptıktan sonra tekrar fatura profiline yönlendirmek için alınan url
#     # login formu ,accounts ve carts componenti olarak iki yerde kullanılmaktadır.
#     next_post=request.POST.get('next')
#     redirect_path=next_ or next_post or None
#     if form.is_valid():
#         # print(form.cleaned_data)
#         username=form.cleaned_data.get('username')
#         password=form.cleaned_data.get('password')
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request,user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path,request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect('/')
#         else:
#             print("ERROR")
#
#     return render(request,'accounts/login.html',context)


class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = "/login/"

class UserDetailUpdateView(LoginRequiredMixin,UpdateView):
    form_class =UserDetailChangeForm
    template_name = "accounts/detail-update-view.html"
    # success_url = "/account/"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self,*args, **kwargs):
        content=super(UserDetailUpdateView,self).get_context_data(*args,**kwargs)
        content['title']="Change Your Account  Details"
        return content

    def get_success_url(self):
        return reverse("account:home")


# User=get_user_model()
# def register_page(request):
#     form=RegisterForm(request.POST or None)
#     context = {
#         'form': form,
#     }
#     if form.is_valid():
#         form.save()
#         # username = form.cleaned_data.get('username')
#         # email = form.cleaned_data.get('email')
#         # password = form.cleaned_data.get('password')
#         # user=User.objects.create_user(username=username,email=email,password=password)
#     return render(request,'accounts/register.html',context)







