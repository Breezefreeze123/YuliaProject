from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Sum, Avg, Max, Min
from django.views import View
from django.views.generic import TemplateView

from .models import Coffee, Category, TagTable, Gost, UploadFiles
from .forms import AddProductForm, UploadFileForm
import uuid
import datetime
import time

main_menu = [
    {'title': 'Main', 'url_name': 'home'},
    {'title': 'Menu', 'url_name': 'menu'},
    {'title': 'News', 'url_name': 'news'},
    {'title': 'Contacts', 'url_name': 'contacts'},
    {'title': 'Add product', 'url_name': 'add_product'},
    {'title': 'Sign in', 'url_name': 'signin'},
]

def home(request):
    data = {
        'title': 'Homepage of Yulia Coffeeshop',
        'main_menu': main_menu,
    }
    return render(request, 'home.html', context=data)

""" Заменена на CBW Menu >>>
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
"""
    
class Menu(TemplateView):
    template_name = 'menu/menu.html'
    extra_context = {
        'title': 'Coffee Menu',
        'title_tags': 'Тэги: ',
        #Проверка, что количество категорий в Category, связанных со статьями в Coffee, больше нуля
        'all_categories': Category.objects.annotate(total=Count('category')).filter(total__gt=0),
        'main_menu': main_menu,
        #Проверка, что количество тэгов в TagTable, связанных со статьями в Coffee, больше нуля
        'all_tags': TagTable.objects.annotate(total=Count('tagtable')).filter(total__gt=0),
    }

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

def handle_uploaded_file(f):
    #new_rename = str(uuid.uuid4()) + f.name
    
    date_time = datetime.datetime.now()
    date_time_format = f'{str(date_time.strftime("%d"))}_{str(date_time.strftime("%b"))}_{str(date_time.strftime("%H"))}_{str(date_time.strftime("%M"))}_{str(date_time.strftime("%S"))}'
    new_rename = f'{date_time_format}_{f.name}'

    
    with open(f"uploads/{new_rename}", "wb+") as destination:
        
        for chunk in f.chunks():
            destination.write(chunk)

""" Заменена на CBW News >>>
def news(request):

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                # Стандартная загрузка файлов
                # handle_uploaded_file(form.cleaned_data['file'])
                
                # Загрузка файлов через модель
                instance = UploadFiles(upload=form.cleaned_data['file'])
                instance.save()
            except Exception as e:
                form.add_error(None, "Ошибка загрузки файла")
                form.add_error(None, e)

    else:
        form = UploadFileForm()    
        

    data = {
        'title': 'Coffee News',
        'main_menu': main_menu,
        'form': form,
    }
    return render(request, 'news/news.html', context=data)
"""
    
class News(View):
    def get(self, request):
        form = UploadFileForm()
        data = {
            'title': 'Coffee News',
            'main_menu': main_menu,
            'form': form,
        }
        return render(request, 'news/news.html', context=data)

    def post(self, request):
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            try:            
                # Загрузка файлов через модель
                instance = UploadFiles(upload=form.cleaned_data['file'])
                instance.save()
            except Exception as e:
                form.add_error(None, "Ошибка загрузки файла")
                form.add_error(None, e)
        data = {
            'title': 'Coffee News',
            'main_menu': main_menu,
            'form': form,
        }
        return render(request, 'news/news.html', context=data)

def contacts(request):
    data = {
        'title': 'Coffeeshop contacts',
        'main_menu': main_menu,
    }
    return render(request, 'contacts/contacts.html', context=data)

def add_product(request):
    
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                #Простой вывод словаря со всеми полями формы в командную строку, заменили на вывод в БД
                #print(form.cleaned_data)
                              
                #Внесение записей из формы в БД, если названия полей в форме полностью соответствуют названиям полей в модели.
                #Заменила на внесение по каждому полю, чтобы настроить связи ManyToMany и OneToOne
                #Coffee.objects.create(**form.cleaned_data)
                
                Coffee.objects.create(title=form.cleaned_data['title'],
                                      slug=form.cleaned_data['slug'],
                                      content=form.cleaned_data['content'], 
                                      is_published=form.cleaned_data['is_published'], 
                                      cat=form.cleaned_data['cat'],
                                      photo=form.cleaned_data['photo'],
                                      )

                Gost.objects.create(gost_product=form.cleaned_data['title'],
                                    gost_number=form.cleaned_data['gost'],
                                    )

                #Связывание Coffee и TagTable через ManyToManyField
                new_coffee = Coffee.objects.get(slug=form.cleaned_data['slug'])
                lst_tag = list(form.cleaned_data['tag'])
                new_coffee.tag.set(lst_tag)               

                #Связывание Coffee и Gost через OneToOneField
                new_gost = Gost.objects.get(gost_number=form.cleaned_data['gost'])
                new_coffee.gost = new_gost
                new_coffee.save()

                

            except Exception as e:
                form.add_error(None, "Ошибка добавления продукта")
                form.add_error(None, e)
    else:
        form = AddProductForm()

    data = {
        'title': 'Add product',
        'main_menu': main_menu,
        'form': form,
    }
    return render(request, 'add_product/add_product.html', context=data)

""" Заменена на CBW SignIn >>>
def signin(request):
    data = {
        'title': 'Sign in',
        'main_menu': main_menu,
    }
    return render(request, 'signin/signin.html', context=data)
"""
""" Заменена на CBW SignIn через TemplateView >>>
class SignIn(View):
    def get(self, request):
        data = {
            'title': 'Sign in',
            'main_menu': main_menu,
        }
        return render(request, 'signin/signin.html', context=data)

    def post(self, request):
        pass
"""
class SignIn(TemplateView):
    template_name = 'signin/signin.html'
    extra_context = {
        'title': 'Sign in',
        'main_menu': main_menu,
    }
