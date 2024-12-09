from django.db import models

# Create your models here.
class Coffee(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField()

    def __str__(self):
        return self.title