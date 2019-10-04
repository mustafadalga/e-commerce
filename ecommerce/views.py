from django.contrib.auth import authenticate, login,get_user_model
from django.shortcuts import redirect,render
from .forms import ContactForm#,LoginForm,RegisterForm
from django.http import HttpResponse,JsonResponse

def home(request):
    # print(request.session.get('first_name',"Tanınmayan"))
    context={
        "mesaj":"Anasayfa"
    }

    if request.user.is_authenticated:
        context['premium']="PREMIUM İÇERİK"
    return render(request,'home.html',context)

def about(request):
    context={
        "mesaj":"Hakkımda"
    }
    return render(request,'home.html',context)


def contact(request):
    contact_form=ContactForm(request.POST or None) # POST edildiğinde değerlerin silinmemesini sağlar.
    context = {
        "mesaj": "İletişim",
        'form':contact_form,
    }
    if contact_form.is_valid():# Eğer form varsa
        # print(contact_form.cleaned_data) #Form verilerini yazdırma
        if request.is_ajax():
            return JsonResponse({
                "message":"Thank you for submission!"
            })

    if contact_form.errors:# Eğer form varsa
        errors=contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors,status=400,content_type="application/json")


    return render(request,'contact/view.html',context)

