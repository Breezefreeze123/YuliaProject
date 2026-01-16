from django.test import TestCase, SimpleTestCase
from django.urls import reverse, resolve
from yulia_app_1.views import show_agreement, Home

# Create your tests here.

class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        self.assertEquals(resolve(url).func.view_class, Home)

    def test_show_agreement_url_is_resolved(self):
        url = reverse('show_agreement',args=[1])
        # print (resolve(url)) 
        self.assertEquals(resolve(url).func, show_agreement)

    