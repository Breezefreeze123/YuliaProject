from django.shortcuts import render
from django.http import HttpResponse


main_sections = [
    {'title': 'Main', 'url_name': 'home'},
    {'title': 'Menu', 'url_name': 'menu'},
    {'title': 'News', 'url_name': 'news'},
    {'title': 'Contacts', 'url_name': 'contacts'},
    {'title': 'Sign in', 'url_name': 'signin'},
]

def home(request):
    data = {
        'title': 'Homepage of Yulia Coffeeshop',
        'main_menu': main_sections,
    }
    return render(request, 'home.html', context=data)

