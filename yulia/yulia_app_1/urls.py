from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name = 'home'),
    path('menu/', views.Menu.as_view(), name = 'menu'),
    path('news/', views.News.as_view(), name = 'news'),
    path('contacts/', views.Contacts.as_view(), name = 'contacts'),
    path('add_product/', views.AddProduct.as_view(), name = 'add_product'), 
    path('edit_product/<slug:slug>', views.EditProduct.as_view(), name = 'edit_product'),
    path('delete_product/<slug:slug>', views.DeleteProduct.as_view(), name = 'delete_product'),
    # path('signin/', views.SignIn.as_view(), name = 'signin'),
    path('menu/<slug:menu_slug>/', views.ShowMenu.as_view(), name = 'show_menu'),
    path('menu/category/<slug:cat_slug>/', views.ShowCategory.as_view(), name = 'show_category'),
    path('menu/tag/<slug:tag_slug>/', views.ShowTag.as_view(), name = 'show_tag'),
    path('add_agreement/', views.AddAgreement.as_view(), name = 'add_agreement'),
    path('show_agreement/<int:pk_agreement>', views.show_agreement, name = 'show_agreement'),
    path('pdf_agreement/<int:pk_agreement>', views.pdf_agreement, name = 'pdf_agreement'),
    path('generate_qr/<int:pk_agreement>', views.generate_qr, name = 'generate_qr'),
    path('get_rate_USD/', views.get_rate_USD, name = 'get_rate_USD'),


]