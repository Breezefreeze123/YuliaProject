from django.db import models
from django.urls import reverse

# Create your models here.
class Coffee(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField()

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('show_menu', kwargs={'menu_slug': self.slug})