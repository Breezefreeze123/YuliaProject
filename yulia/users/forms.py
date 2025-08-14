from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Имя',
                            widget=forms.TextInput())
    password = forms.CharField(label='Пароль',
                            widget=forms.PasswordInput())

    class Meta:
        # Через get_user_model() по дефолту идет связка на модель Users 
        model = get_user_model()
        fields = ['username', 'password']