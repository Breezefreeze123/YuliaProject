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
    is_published = models.BooleanField(choices=Status, default=Status.PUBLISHED)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='category')
    tag = models.ManyToManyField('TagTable', blank=True, related_name='tagtable')

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('show_menu', kwargs={'menu_slug': self.slug})
    
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('show_category', kwargs={'cat_slug': self.slug})
    
class TagTable(models.Model):
    tag = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.tag
    
    def get_absolute_url(self):
        return reverse('show_tag', kwargs={'tag_slug': self.slug})