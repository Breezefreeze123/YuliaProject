from django.shortcuts import render
from django.http import HttpResponse

main_sections = [
    {'title': 'Main', 'url_name': 'home'},
    {'title': 'Menu', 'url_name': 'menu'},
    {'title': 'News', 'url_name': 'news'},
    {'title': 'Contacts', 'url_name': 'contacts'},
    {'title': 'Sign in', 'url_name': 'signin'},
]

#Позже заменится на базу данных:
data_coffee = [
    {'id': 1, 'title': 'Food', 'content': 'Club sandwich, Caesar salad, Sushi', 'is_published': True},
    {'id': 2, 'title': 'Drinks', 'content': 'Cappuchino, Espresso, Earl gray tea', 'is_published': True},
    {'id': 3, 'title': 'Deserts', 'content': 'Tiramisu, Mango cheesecake, Brauni', 'is_published': True},
]

def home(request):
    data = {
        'title': 'Homepage of Yulia Coffeeshop',
        'main_menu': main_sections,
    }
    return render(request, 'home.html', context=data)

def menu(request):
    data = {
        'title': 'Coffee Menu',
        'menu_sections': data_coffee,
        'main_menu': main_sections,
    }
    return render(request, 'menu/menu.html', context=data)

def show_menu(request, menu_section):
    data = {
        'title': f'Раздел меню под наименованием {menu_section}',
        'main_menu': main_sections,
    }
    return render(request, 'menu/menu_sections.html', context=data)

def news(request):
    data = {
        'title': 'Coffee News',
        'main_menu': main_sections,
    }
    return render(request, 'news/news.html', context=data)

def contacts(request):
    data = {
        'title': 'Coffeeshop contacts',
        'main_menu': main_sections,
    }
    return render(request, 'contacts/contacts.html', context=data)

def signin(request):
    data = {
        'title': 'Sign in',
        'main_menu': main_sections,
    }
    return render(request, 'signin/signin.html', context=data)