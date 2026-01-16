from django.test import TestCase, Client
from django.urls import reverse, resolve
from yulia_app_1.models import Coffee, Category, TagTable
import json

# Create your tests here.

class TestViews(TestCase):

    fixtures = ["category.json", "client.json", "coffee.json", 
                "gost.json", "tagtable.json", "uploadfiles.json"]

    def test_Home_view(self):
        path = reverse('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        # Или проверка на возврат корректного html может осуществляться через assertIn:
        # self.assertIn('home.html', response.template_name)
        self.assertEqual(response.context_data['title'],'Homepage of Yulia Coffeeshop')

    def test_ShowCategory_database(self):
        path = reverse('show_category')
        response = self.client.get(path)
        coffee_pub = Coffee.objects.all().filter(is_published=1)
        self.assertQuerySetEqual(response.context_data['all_products'], coffee_pub)


    def test_pdf_agreement_GET(self):
        client = Client()
        response = client.get(reverse('pdf_agreement', args=[1]))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_agreement/pdf_agreement.html')