from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Sum, Avg, Max, Min

from .models import Coffee, Category, TagTable

main_menu = [
    {'title': 'Main', 'url_name': 'home'},
    {'title': 'Menu', 'url_name': 'menu'},
    {'title': 'News', 'url_name': 'news'},
    {'title': 'Contacts', 'url_name': 'contacts'},
    {'title': 'Sign in', 'url_name': 'signin'},
]

def home(request):
    data = {
        'title': 'Homepage of Yulia Coffeeshop',
        'main_menu': main_menu,
    }
    return render(request, 'home.html', context=data)

def menu(request):

    all_categories = Category.objects.annotate(total=Count('category')).filter(total__gt=0) #Проверка, что количество категорий в Category, связанных со статьями в Coffee, больше нуля
    all_tags = TagTable.objects.annotate(total=Count('tagtable')).filter(total__gt=0) #Проверка, что количество тэгов в TagTable, связанных со статьями в Coffee, больше нуля
  
    data = {
        'title': 'Coffee Menu',
        'title_tags': 'Тэги: ',
        'all_categories': all_categories,
        'main_menu': main_menu,
        'all_tags': all_tags,
    }
    return render(request, 'menu/menu.html', context=data)

def show_category(request, cat_slug):

    all_categories = Category.objects.annotate(total=Count('category')).filter(total__gt=0) #Проверка, что количество категорий в Category, связанных со статьями в Coffee, больше нуля
    all_tags = TagTable.objects.annotate(total=Count('tagtable')).filter(total__gt=0) #Проверка, что количество тэгов в TagTable, связанных со статьями в Coffee, больше нуля

    category = get_object_or_404(Category, slug=cat_slug)
    post = Coffee.objects.filter(cat_id=category.pk)

    data = {
        'title': f'Раздел: {category.title}',
        'title_tags': 'Тэги: ',
        'all_categories': all_categories,
        'main_menu': main_menu,
        'category': category,
        'post': post,
        'all_tags': all_tags,
        
    }
    return render(request, 'menu/menu.html', context=data)

def show_tag(request, tag_slug):

    all_categories = Category.objects.annotate(total=Count('category')).filter(total__gt=0) #Проверка, что количество категорий в Category, связанных со статьями в Coffee, больше нуля
    all_tags = TagTable.objects.annotate(total=Count('tagtable')).filter(total__gt=0) #Проверка, что количество тэгов в TagTable, связанных со статьями в Coffee, больше нуля

    tag = get_object_or_404(TagTable, slug=tag_slug)
    tag_selection = tag.tagtable.all()

    data = {
        'title': f'Тэг: {tag.tag}',
        'title_tags': 'Тэги: ',
        'main_menu': main_menu,
        'all_categories': all_categories,
        'all_tags': all_tags,
        'tag': tag,
        'tag_selection': tag_selection,
    }
    return render(request, 'menu/menu.html', context=data)

def show_menu(request, menu_slug):

    all_categories = Category.objects.annotate(total=Count('category')).filter(total__gt=0) #Проверка, что количество категорий в Category, связанных со статьями в Coffee, больше нуля
    all_tags = TagTable.objects.annotate(total=Count('tagtable')).filter(total__gt=0) #Проверка, что количество тэгов в TagTable, связанных со статьями в Coffee, больше нуля

    post = get_object_or_404(Coffee, slug=menu_slug)

    data = {
        'title_tags': 'Тэги: ',
        'post': post,
        'main_menu': main_menu,
        'all_categories': all_categories,
        'all_tags': all_tags,
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