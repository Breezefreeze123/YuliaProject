from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def signin(request):
    data = {
        'title': 'Sign in',
    }
    return render(request, 'signin/signin.html', context=data)
