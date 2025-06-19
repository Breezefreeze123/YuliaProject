from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout

from .forms import LoginUserForm

main_menu = [
    {'title': 'Main', 'url_name': 'home'},
    {'title': 'Menu', 'url_name': 'menu'},
    {'title': 'News', 'url_name': 'news'},
    {'title': 'Contacts', 'url_name': 'contacts'},
    {'title': 'Add product', 'url_name': 'add_product'},
    {'title': 'Log in', 'url_name': 'users:login'},
    {'title': 'Log out', 'url_name': 'users:logout'},
]

def login_user(request):
    if request.method == 'POST':
        form = LoginUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user:
                login(request, user)
                return HttpResponseRedirect(reverse('menu'))
    else:
        form = LoginUserForm()

    data={
        'title': 'Log in',
        'main_menu': main_menu,
        'form': form,
    }

    return render(request, 'login_logout/login.html', context=data)

# class LogIn(FormView):
#     template_name = 'login_logout/login.html'
#     form_class = LoginUserForm
#     success_url = reverse_lazy('menu')
#     extra_context = {
#         'title': 'Log in',
#         'main_menu': main_menu,
#     }

#     def form_valid(self, form):
#         user = authenticate(username='username', password='password')
#         if user and user.is_active:
#             login(request, user)
#         return super().form_valid(form)

def logout_user(request):
    logout(request)

    data={
        'title': 'Log in',
        'main_menu': main_menu,
    }

    return HttpResponseRedirect(reverse('users:login'))

# class LogOut(TemplateView):
#     template_name = 'login_logout/logout.html'
#     extra_context = {
#         'title': 'Log out',
#         'main_menu': main_menu,
#     }
