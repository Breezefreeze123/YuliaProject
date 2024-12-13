from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('menu/', views.menu, name = 'menu'),
    path('news/', views.news, name = 'news'),
    path('contacts/', views.contacts, name = 'contacts'),
    path('signin/', views.signin, name = 'signin'),
    path('menu/<slug:menu_slug>/', views.show_menu, name = 'show_menu'),
    path('menu/category/<slug:cat_slug>/', views.show_category, name = 'show_category'),
]