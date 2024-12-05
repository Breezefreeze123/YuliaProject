from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def contacts(request):
    data = {
        'title': 'Coffeeshop contacts',
    }
    return render(request, 'contacts/contacts.html', context=data)

