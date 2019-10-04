from django.contrib.auth import authenticate, login,get_user_model
from django.shortcuts import redirect,render
from django.views.generic import CreateView,FormView
from .forms import LoginForm,RegisterForm,GuestForm
from django.utils.http import is_safe_url
from .models import GuestEmail
from .signals import user_logged_in



def guest_register_view(request):
    form=GuestForm(request.POST or None)
    context = {
        'form': form,
    }
    next_=request.GET.get('next')
    next_post=request.POST.get('next')
    redirect_path=next_ or next_post or None
    if form.is_valid():
        email=form.cleaned_data.get('email')
        new_guest_email=GuestEmail.objects.create(email=email)
        request.session['guest_email_id']=new_guest_email.id
        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('/register/')
    return redirect('/register/')



class LoginView(FormView):
    form_class = LoginForm
    template_name = "accounts/login.html"
    success_url = "/"

    def form_valid(self, form):
        request=self.request
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            user_logged_in.send(user.__class__, instance=user, request=request)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect('/')
        return super(LoginView,self).form_invalid(form)
#
# def login_page(request):
#     form=LoginForm(request.POST or None)
#     context = {
#         'form': form,
#     }
#     # print(request.user.is_authenticated)
#     next_=request.GET.get('next')
#
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







