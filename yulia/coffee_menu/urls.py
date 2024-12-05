from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu, name = 'menu'),
    path('<slug:menu_section>/', views.show_menu, name = 'show_menu'),

]