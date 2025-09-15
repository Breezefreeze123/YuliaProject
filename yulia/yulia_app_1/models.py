from django.db import models
from django.urls import reverse

# Create your models here.
class Coffee(models.Model):

    class Status(models.IntegerChoices):
        DRAFT = 0
        PUBLISHED = 1

    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status, default=Status.DRAFT)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='category')
    tag = models.ManyToManyField('TagTable', blank=True, related_name='tagtable')
    gost = models.OneToOneField('Gost', on_delete=models.SET_NULL, null=True, blank=True, related_name='gost')
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, null=True)

    class Meta:
        verbose_name='Продуктовые позиции для кофейни'
        verbose_name_plural='Продуктовые позиции для кофейни'

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('show_menu', kwargs={'menu_slug': self.slug})
    
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name='Категории меню'
        verbose_name_plural='Категории меню'

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('show_category', kwargs={'cat_slug': self.slug})
    
class TagTable(models.Model):
    tag = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name='Тэги'
        verbose_name_plural='Тэги'

    def __str__(self):
        return self.tag
    
    def get_absolute_url(self):
        return reverse('show_tag', kwargs={'tag_slug': self.slug})
    
class Gost(models.Model):
    gost_product = models.CharField(max_length=50)
    gost_number = models.IntegerField()

    def __str__(self):
        return self.gost_product
    
class UploadFiles(models.Model):
    upload = models.FileField(upload_to="uploads_model/")
    
    def __str__(self):
        return self.upload    

class Client(models.Model):
    
    name = models.CharField(max_length=50)
    passport_num = models.IntegerField(unique=True)
    agreement_num = models.CharField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    agreement_date = models.DateField(auto_now_add=True)
    quantity = models.FloatField(blank=False, default=1)
    email = models.EmailField(max_length=100, blank=False)
    
    class Meta:
        verbose_name='Реквизиты клиентов'
        verbose_name_plural='Реквизиты клиентов'

    def __str__(self):
        return self.name