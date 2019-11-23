from django.shortcuts import redirect,render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView,FormView,DetailView,View,UpdateView
from django.views.generic.edit import FormMixin
from .forms import LoginForm,RegisterForm,GuestForm,ReactiveEmailForm,UserDetailChangeForm
from ecommerce.mixins import NextUrlMixin,RequestFormAttachMixin

from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import EmailActivation


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


class LoginView(NextUrlMixin,RequestFormAttachMixin,FormView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    success_url = "/"
    default_next = "/"

    def form_valid(self, form):
        next_path=self.get_next_url()
        return redirect(next_path)




class RegisterView(CreateView):
    form_class = RegisterForm
    template_name = 'accounts/register.html'
    success_url = "/login/"

class UserDetailUpdateView(LoginRequiredMixin,UpdateView):
    form_class =UserDetailChangeForm
    template_name = "accounts/detail-update-view.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self,*args, **kwargs):
        content=super(UserDetailUpdateView,self).get_context_data(*args,**kwargs)
        content['title']="Change Your Account  Details"
        return content

    def get_success_url(self):
        return reverse("account:home")









