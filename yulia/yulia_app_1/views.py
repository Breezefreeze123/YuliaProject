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
from django.template.loader import get_template
from xhtml2pdf import pisa
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# from reportlab.lib.units import inch

# Импорт для генерации qr для договора 
import qrcode

# Импорт для подгрузки курсов валют
import requests
import json

# Импорт для отправки емейл
from django.core.mail import EmailMultiAlternatives, send_mail, EmailMessage
from django.template.loader import render_to_string

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
    
class AddAgreement(FormView):
    template_name = 'add_agreement/add_agreement.html'
    form_class = AddClientForm
    #success_url = reverse_lazy('show_client_agreement')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add client credentials'
        return context

    def form_valid(self, form):
        # Создание записи в БД
        new_client = Client.objects.create(name=form.cleaned_data['name'],
                              passport_num=form.cleaned_data['passport_num'],
                              agreement_num=form.cleaned_data['agreement_num'],
                              quantity=form.cleaned_data['quantity'],
                              email=form.cleaned_data['email'],
                             )
        self.success_url = reverse_lazy('show_agreement', kwargs={'pk_agreement':new_client.pk})

        return super().form_valid(form)
         
def get_rate_USD():
    url = 'https://api.currencyfreaks.com/v2.0/rates/latest?apikey=1cebcc463e9a4760bc348fdcb09e8789'

    try:
        # Получаем содержимое страницы
        response = requests.get(url)
        response.raise_for_status()

        # Парсинг содержимого страницы с помощью надстройки json
        rates = json.loads(response.content)
        USD_rate = float(rates["rates"]["RUB"])

    except requests.exceptions.RequestException as e:
        print(f'Ошибка при запросе: {e}')
    return USD_rate

def show_agreement(request, pk_agreement):

    new_client = get_object_or_404(Client,pk=pk_agreement)
    price_RUB = 100
    price_USD = round(price_RUB/ get_rate_USD(),4)

    context = {
        'title': 'Agreement preview',
        'new_client': new_client,
        'price_RUB': price_RUB,
        'amount_RUB': price_RUB * new_client.quantity,
        'price_USD': price_USD, 
        'amount_USD': round(price_USD * new_client.quantity,4),
    }
    return render(request, 'add_agreement/show_agreement.html', context)

def pdf_agreement_buffer(title, new_client, price_RUB, amount_RUB, price_USD, amount_USD):
    buffer = io.BytesIO()
    template_path = 'add_agreement/pdf_agreement.html'

    context = {
        'title': title,
        'new_client': new_client,
        'price_RUB': price_RUB,
        'amount_RUB': amount_RUB,
        'price_USD': price_USD, 
        'amount_USD': amount_USD,
    }    

    template = get_template(template_path)
    html = template.render(context)

    pisa.CreatePDF(
        html,           # page data
        dest=buffer,    # destination "file"
    )

    return buffer.getbuffer()

def pdf_agreement_request(request, pk_agreement):

    title = 'Agreement'
    new_client = get_object_or_404(Client,pk=pk_agreement)
    price_RUB = 100
    amount_RUB = price_RUB * new_client.quantity
    price_USD = round(price_RUB/ get_rate_USD(),4)
    amount_USD = round(price_USD * new_client.quantity,4)
    
    buffer = pdf_agreement_buffer(title, new_client, price_RUB, amount_RUB, price_USD, amount_USD)

    return HttpResponse(buffer, content_type = 'application/pdf')

def pdf_agreement_request_old(request, pk_agreement):
    template_path = 'add_agreement/pdf_agreement.html'
    
    new_client = get_object_or_404(Client,pk=pk_agreement)
    price_RUB = 100
    price_USD = round(price_RUB/ get_rate_USD(),4)

    context = {
        'title': 'Agreement',
        'new_client': new_client,
        'price_RUB': price_RUB,
        'amount_RUB': price_RUB * new_client.quantity,
        'price_USD': price_USD, 
        'amount_USD': round(price_USD * new_client.quantity,4),
    }

    # Create a Django response object, setting the PDF as the content type
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="Agreement.pdf"'

    # Render the HTML template
    template = get_template(template_path)
    html = template.render(context)

    # html_source = "<html><body><p>To PDF or not to PDF</p></body></html>"

    # Convert HTML to PDF
    pisa_status = pisa.CreatePDF(
        html,                # the HTML to convert
        dest=response)       # file handle to receive result

    # If error, show an error page
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

def generate_qr(request, pk_agreement):
    new_client = get_object_or_404(Client,pk=pk_agreement)

    img = qrcode.make(f'Agreement number: {new_client.agreement_num}, Agreement date: {new_client.agreement_date}')
    buffer = io.BytesIO()
    img.save(buffer, format="png")
    return HttpResponse(buffer.getvalue(), content_type = 'image/png')

def generate_email_test(request):
    send_mail(
        "Yulia Agreement",
        "Here is the message.",
        "loskutova.yulia@gmail.com",
        ["loskutova.yulia@gmail.com"],
        fail_silently=False,
    )
    return HttpResponse('Email sent!')

def generate_email(request, pk_agreement):
    new_client = get_object_or_404(Client,pk=pk_agreement)

    email = EmailMessage(
        subject = f"Agreement № {new_client.agreement_num}",
        body = f"Hello, {new_client.name}, your agreement № {new_client.agreement_num} is enclosed.",
        from_email = "loskutova.yulia@gmail.com",
        to = ["loskutova.yulia@gmail.com"],
    )

    title = 'Agreement'
    new_client = get_object_or_404(Client,pk=pk_agreement)
    price_RUB = 100
    amount_RUB = price_RUB * new_client.quantity
    price_USD = round(price_RUB/ get_rate_USD(),4)
    amount_USD = round(price_USD * new_client.quantity,4)
    
    new_pdf = pdf_agreement_buffer(title, new_client, price_RUB, amount_RUB, price_USD, amount_USD)
    email.attach(f"Agreement № {new_client.agreement_num}.pdf", new_pdf, "application/pdf")
    
    email.send()

    context = {
        'title': 'Email successfully sent',
        'new_client': new_client,
    }

    return render(request, 'add_agreement/return.html', context)
