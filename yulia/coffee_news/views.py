from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def news(request):
    data = {
        'title': 'Coffee News',
    }
    return render(request, 'news/news.html', context=data)