from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name = 'home'),
    path('menu/', views.Menu.as_view(), name = 'menu'),
    path('news/', views.News.as_view(), name = 'news'),
    path('contacts/', views.Contacts.as_view(), name = 'contacts'),
    path('add_product/', views.add_product, name = 'add_product'), 
    path('signin/', views.SignIn.as_view(), name = 'signin'),
    path('menu/<slug:menu_slug>/', views.ShowMenu.as_view(), name = 'show_menu'),
    path('menu/category/<slug:cat_slug>/', views.ShowCategory.as_view(), name = 'show_category'),
    path('menu/tag/<slug:tag_slug>/', views.ShowTag.as_view(), name = 'show_tag'),
]