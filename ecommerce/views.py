from django.shortcuts import render
from .forms import ContactForm
from django.http import HttpResponse,JsonResponse

def home(request):
    context={
        "mesaj":"Ecommerce Project"
    }
    return render(request,'home.html',context)

def about(request):
    context={
        "mesaj":"Hakkımda"
    }
    return render(request,'home.html',context)


def contact(request):
    contact_form=ContactForm(request.POST or None)
    context = {
        "mesaj": "İletişim",
        'form':contact_form,
    }
    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({
                "message":"Thank you for submission!"
            })

    if contact_form.errors:
        errors=contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors,status=400,content_type="application/json")
    return render(request,'contact/view.html',context)

