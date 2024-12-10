from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Coffee

main_menu = [
    {'title': 'Main', 'url_name': 'home'},
    {'title': 'Menu', 'url_name': 'menu'},
    {'title': 'News', 'url_name': 'news'},
    {'title': 'Contacts', 'url_name': 'contacts'},
    {'title': 'Sign in', 'url_name': 'signin'},
]

#Заменено на базу данных:
data_coffee = [
    {'id': 1, 'title': 'Food', 'content': 'Club sandwich, Caesar salad, Sushi', 'is_published': True},
    {'id': 2, 'title': 'Drinks', 'content': 'Cappuchino, Espresso, Earl gray tea', 'is_published': True},
    {'id': 3, 'title': 'Deserts', 'content': 'Tiramisu, Mango cheesecake, Brauni', 'is_published': True},
]

def home(request):
    data = {
        'title': 'Homepage of Yulia Coffeeshop',
        'main_menu': main_menu,
    }
    return render(request, 'home.html', context=data)

def menu(request):

    post = Coffee.objects.all()

    data = {
        'title': 'Coffee Menu',
    #    'menu_sections': data_coffee,
        'post': post,
        'main_menu': main_menu,
    }
    return render(request, 'menu/menu.html', context=data)

def show_menu(request, menu_slug):

    post = get_object_or_404(Coffee, slug=menu_slug)

    data = {
        'post': post,
        'main_menu': main_menu,
    }
    return render(request, 'menu/menu_sections.html', context=data)

def news(request):
    data = {
        'title': 'Coffee News',
        'main_menu': main_menu,
    }
    return render(request, 'news/news.html', context=data)

def contacts(request):
    data = {
        'title': 'Coffeeshop contacts',
        'main_menu': main_menu,
    }
    return render(request, 'contacts/contacts.html', context=data)

def signin(request):
    data = {
        'title': 'Sign in',
        'main_menu': main_menu,
    }
    return render(request, 'signin/signin.html', context=data)