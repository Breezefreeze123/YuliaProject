from django.test import TestCase

# Create your tests here.

class TestSmth(TestCase):

    # Инициализация перед выполнением каждого теста
    def setUp(self):
        return super().setUp()

    def test_smth1(self):
        pass

    def test_smth2(self):
        pass

    # Действия после выполнения каждого теста
    def tearDown(self):
        return super().tearDown()