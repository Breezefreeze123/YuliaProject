from django import forms
from .models import Coffee, Category, TagTable, Client
from django.core.validators import MinLengthValidator, MaxLengthValidator


class AddProductForm(forms.ModelForm):
    #Ручное добавление полей - убрала, т.к. добавила класс ModelForm ниже 
    #title = forms.CharField(min_length=5, max_length=50, label='Заголовок', error_messages={'min_length': 'Слишком короткий заголовок', 'max_length': 'Слишком длинный заголовок'})
    #slug = forms.SlugField(max_length=50, label='Slug', validators=[MinLengthValidator(5, message='Слишком короткий URL'), MaxLengthValidator(50, message='Слишком длинный URL')])
    #content = forms.CharField(required=False, widget=forms.Textarea, label='Содержание')
    #is_published = forms.BooleanField(required=False, label='Опубликовано', initial=1)
    #tag = forms.ModelMultipleChoiceField(queryset=TagTable.objects.all(), label='Тэг', widget=forms.CheckboxSelectMultiple)
    
    #Добавление полей из модели через класс ModelForm
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label=None)
    gost = forms.IntegerField(required=False, label="ГОСТ номер")

    class Meta:
        model = Coffee
        fields = ['title', 'slug', 'content', 'is_published', 'cat', 'tag', 'photo']
        widgets = {
            'tag': forms.CheckboxSelectMultiple,
        }

class UploadFileForm(forms.Form):
    file = forms.FileField()

class AddClientForm(forms.Form):

    name = forms.CharField(max_length=50, label='ФИО: ')
    passport_num = forms.IntegerField(label='Паспорт, номер: ')
    agreement_num = forms.CharField(label='Номер договора: ')
    quantity = forms.FloatField(label='Количество, кг: ')

    # class Meta:
    #     model = Client
    #     fields = ['name', 'passport_num', 'agreement_num', 'quantity']