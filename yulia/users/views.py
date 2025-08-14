from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView, FormView
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm

from .forms import LoginUserForm

# def login_user(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(request, username=cd['username'], password=cd['password'])
#             if user:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('menu'))
#     else:
#         form = LoginUserForm()

#     data={
#         'title': 'Log in',
#         'form': form,
#     }

#     return render(request, 'login_logout/login.html', context=data)

class LoginUser(LoginView):
    template_name = 'login_logout/login.html'
    form_class = LoginUserForm #Внимание! По умолчанию LoginView использует форму AuthenticationForm.
                               #Здесь пишу LoginUserForm, т.к. в forms.py унаследовали LoginUserForm от AuthenticationForm
    extra_context = {
        'title': 'Log in',
    }

    # Есть два метода перенаправления при успешной авторизации.
    # Первый ниже при использовании метода get_success_url.
    # Второй (использован) в добавлении пути в LOGIN_REDIRECT_URL в файле settings.py
    # def get_success_url(self):
    #     return reverse_lazy('menu')

# def logout_user(request):
#     logout(request)

#     data={
#         'title': 'Log in',
#     }

#     return HttpResponseRedirect(reverse('users:login'))

class LogoutUser(LogoutView):
    template_name = 'login_logout/logout.html'
    # form_class = LoginUserForm #Внимание! По умолчанию LoginView использует форму AuthenticationForm.
    #                            #Здесь пишу LoginUserForm, т.к. в forms.py унаследовали LoginUserForm от AuthenticationForm
    extra_context = {
        'title': 'Log out',
    }