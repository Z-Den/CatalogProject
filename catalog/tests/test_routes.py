from django.test import TestCase, Client
from django.urls import reverse
from catalog.models import Product, Category
from django.contrib.auth.models import User

class RouteTests(TestCase):
    def setUp(self):
        self.client = Client()
        
        # Создаем категорию
        self.category = Category.objects.create(name='натуральный')
        
        # Создаем продукт
        self.product = Product.objects.create(
            brand="Test Brand",
            sugar_content=10,
            volume=1,
            is_alcoholic=False,
            flavor="Test Flavor",
            category=self.category
        )
        
        self.client.login(username='admin', password='admin') 

    def test_home_page_status(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.brand)

    def test_product_detail_page_status(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.product.brand)

    def test_product_edit_page_status(self):
        response = self.client.get(reverse('product_edit', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_product_create_page_status(self):
        response = self.client.get(reverse('product_create'))
        self.assertEqual(response.status_code, 200)

    def test_add_to_cart_redirect(self):
        response = self.client.get(reverse('add_to_cart', args=[self.product.id]))
        self.assertEqual(response.status_code, 302)

    def test_cart_detail_page_status(self):
            self.client.login(username='admin', password='admin')
            response = self.client.get(reverse('cart_detail'))
            self.assertEqual(response.status_code, 404)

    def test_about_page_status(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "О сервисе")

    def test_nonexistent_page(self):
        response = self.client.get('/nonexistent/')
        self.assertEqual(response.status_code, 404)