from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('menu/', views.menu, name = 'menu'),
    path('news/', views.news, name = 'news'),
    path('contacts/', views.contacts, name = 'contacts'),
    path('signin/', views.signin, name = 'signin'),
    path('<slug:menu_section>/', views.show_menu, name = 'show_menu'),
    
]