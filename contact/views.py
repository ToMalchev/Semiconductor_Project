from django.shortcuts import render
from .models import contactDetail

def contact(request):
    contact_dict = {}
    try:
        contact = contactDetail.objects.last()
        contact_dict = {'name': contact.name, 'telephone': contact.tel, 'address': contact.addr}
    except:
        contact_dict = {'name': '', 'telephone': '', 'address': ''}
    return render(request, 'contact/contact.html', contact_dict)