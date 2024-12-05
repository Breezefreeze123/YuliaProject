from django.shortcuts import render
from django.http import HttpResponse

#Позже заменится на базу данных:
data_coffee = [
    {'id': 1, 'title': 'Food', 'content': 'Club sandwich, Caesar salad, Sushi', 'is_published': True},
    {'id': 2, 'title': 'Drinks', 'content': 'Cappuchino, Espresso, Earl gray tea', 'is_published': True},
    {'id': 3, 'title': 'Deserts', 'content': 'Tiramisu, Mango cheesecake, Brauni', 'is_published': True},
]

def menu(request):
    data = {
        'title': 'Coffee Menu',
        'menu_sections': data_coffee,
    }
    return render(request, 'menu/menu.html', context=data)

def show_menu(request, menu_section):
    data = {
        'title': f'Раздел меню под наименованием {menu_section}',
    }
    return render(request, 'menu/menu_sections.html', context=data)
   
