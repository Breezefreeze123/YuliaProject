from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from .models import Coffee, Category

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

    all_categories = Category.objects.all()  
  
    data = {
        'title': 'Coffee Menu',
        'all_categories': all_categories,
        'main_menu': main_menu,
    }
    return render(request, 'menu/menu.html', context=data)

def show_category(request, cat_slug):

    all_categories = Category.objects.all()

    category = get_object_or_404(Category, slug=cat_slug)
    post = Coffee.objects.filter(cat_id=category.pk)

    data = {
        'title': f'Раздел: {category.title}',
        'all_categories': all_categories,
        'main_menu': main_menu,
        'category': category,
        'post': post,
        
    }
    return render(request, 'menu/menu.html', context=data)

def show_menu(request, menu_slug):

    all_categories = Category.objects.all()

    post = get_object_or_404(Coffee, slug=menu_slug)

    data = {
        'post': post,
        'main_menu': main_menu,
        'all_categories': all_categories,
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