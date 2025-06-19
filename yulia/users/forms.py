from django import forms

class LoginUserForm(forms.Form):
    username = forms.CharField(label='Имя',
                            widget=forms.TextInput())
    password = forms.CharField(label='Пароль',
                            widget=forms.PasswordInput())

