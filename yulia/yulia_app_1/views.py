from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Count, Sum, Avg, Max, Min
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.core.paginator import Paginator

from .models import Coffee, Category, TagTable, Gost, UploadFiles, Client
from .forms import AddProductForm, UploadFileForm, AddClientForm
import uuid
import datetime
import time

# Импорт для генерации pdf договора 
import io
from django.http import FileResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

class Home(TemplateView):
    template_name = 'home.html'
    extra_context = {
        'title': 'Homepage of Yulia Coffeeshop',
    }

class Menu(ListView):
    #model = Coffee
    template_name = 'menu/menu.html'
    context_object_name = 'all_products'
    
    extra_context = {
        'title': 'Coffee Menu',
        'title_tags': 'Тэги: ',
        #Проверка, что количество категорий в Category, связанных со статьями в Coffee, больше нуля
        'all_categories': Category.objects.annotate(total=Count('category')).filter(total__gt=0),
        #Проверка, что количество тэгов в TagTable, связанных со статьями в Coffee, больше нуля
        'all_tags': TagTable.objects.annotate(total=Count('tagtable')).filter(total__gt=0),
    }
    
    def get_queryset(self):
        return Coffee.objects.all().filter(is_published=1)

class ShowCategory(ListView):
    template_name = 'menu/menu.html'
    context_object_name = 'post'
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        # return Coffee.objects.filter(cat__slug=self.kwargs['cat_slug'])
        self.category = get_object_or_404(Category, slug=self.kwargs['cat_slug'])
        return Coffee.objects.filter(cat_id=self.category.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # cat = context['post'][0].cat
        # context['title'] = 'Категория: ' + cat.title
        context['title'] = 'Категория: ' + self.category.title
        context['title_tags'] = 'Тэги: '
        context['all_categories'] = Category.objects.annotate(total=Count('category')).filter(total__gt=0)
        context['all_tags'] = TagTable.objects.annotate(total=Count('tagtable')).filter(total__gt=0)
        return context

class ShowTag(ListView):
    template_name = 'menu/menu.html'
    context_object_name = 'tag_selection'
    allow_empty = False
    paginate_by = 3

    def get_queryset(self):
        self.tag = get_object_or_404(TagTable, slug=self.kwargs['tag_slug'])
        return self.tag.tagtable.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Тэг: ' + self.tag.tag
        context['title_tags'] = 'Тэги: '
        context['all_categories'] = Category.objects.annotate(total=Count('category')).filter(total__gt=0)
        context['all_tags'] = TagTable.objects.annotate(total=Count('tagtable')).filter(total__gt=0)
        return context

class ShowMenu(DetailView):
    # model = Coffee
    slug_url_kwarg = 'menu_slug'
    context_object_name = 'post'
    template_name = 'menu/menu_sections.html'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title_tags'] = 'Тэги: '
        context['all_categories'] = Category.objects.annotate(total=Count('category')).filter(total__gt=0)
        context['all_tags'] = TagTable.objects.annotate(total=Count('tagtable')).filter(total__gt=0)
        return context
    
    def get_object(self, queryset = None):
        return get_object_or_404(Coffee, is_published = True, slug=self.kwargs[self.slug_url_kwarg])

class News(FormView):
    template_name = 'news/news.html'
    form_class = UploadFileForm
    success_url = reverse_lazy('menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Coffee News'
        return context
    
class Contacts(TemplateView):
    template_name = 'contacts/contacts.html'
    extra_context = {
        'title': 'Coffeeshop contacts',
    }

class AddProduct(FormView):
    template_name = 'add_product/add_product.html'
    form_class = AddProductForm
    success_url = reverse_lazy('menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add product'
        return context
    
    def form_valid(self, form):
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
        
        return super().form_valid(form)

class EditProduct(UpdateView):
    model = Coffee
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'add_product/add_product.html'
    success_url = reverse_lazy('menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit product'
        return context

class DeleteProduct(DeleteView):
    model = Coffee
    fields = ['title', 'content', 'photo', 'is_published', 'cat']
    template_name = 'add_product/add_product.html'
    success_url = reverse_lazy('menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Delete product'
        return context
    
# Функция добавления pdf из документации. Не используется на сайте: 
def add_agreement(request):
    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    # p.drawString(100,100,'Hello World')

    # Create text object
    textobject = p.beginText()
    textobject.setTextOrigin(inch, inch)

    # Добавляем содержимое
    coffee_lines = Coffee.objects.all()
    lines = []
    for coffee_line in coffee_lines:
        lines.append(coffee_line.title)
        
    for line in lines:
        textobject.textLine(line)

    # Close the PDF object cleanly
    p.drawText(textobject) 
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)

    return FileResponse(buffer, as_attachment=True, filename='hello.pdf')

class AddAgreement(FormView):
    template_name = 'add_agreement/add_agreement.html'
    form_class = AddClientForm
    success_url = reverse_lazy('menu')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add client credentials'
        return context
    
    def form_valid(self, form):
        # Создание записи в БД
        Client.objects.create(name=form.cleaned_data['name'],
                              passport_num=form.cleaned_data['passport_num'],
                              agreement_num=form.cleaned_data['agreement_num'],
                             )

        # Создание pdf
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter, bottomup=0)
        textobject = p.beginText()
        textobject.setTextOrigin(inch, inch)

        client_lines = Client.objects.all()
        lines = []
        for client_line in client_lines:
            lines.append(client_line.name)
            
        for line in lines:
            textobject.textLine(line)

        p.drawText(textobject) 
        p.showPage()
        p.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='Clients.pdf')

        return super().form_valid(form)