main_menu = [
    {'title': 'Main', 'url_name': 'home'},
    {'title': 'Menu', 'url_name': 'menu'},
    {'title': 'News', 'url_name': 'news'},
    {'title': 'Contacts', 'url_name': 'contacts'},
    {'title': 'Add product', 'url_name': 'add_product'},
    {'title': 'Add agreement', 'url_name': 'add_agreement'},
    # {'title': 'Log in', 'url_name': 'users:login'},
    # {'title': 'Log out', 'url_name': 'users:logout'},
]

def get_main_menu(request):
    return {'main_menu': main_menu}