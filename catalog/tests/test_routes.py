from django.test import TestCase, Client
from django.urls import reverse
from catalog.models import Product, Category

class RouteTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Сначала создаем категорию
        self.category = Category.objects.create(
            name='натуральный'
        )
        # Затем создаем продукт с этой категорией
        self.product = Product.objects.create(
            brand="Test Brand",
            sugar_content=10,
            volume=1,
            is_alcoholic=False,
            flavor="Test Flavor",
            category=self.category  # Используем созданную категорию
        )

    def test_home_page_status(self):
        response = self.client.get(reverse('product_list'))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_status(self):
        response = self.client.get(reverse('product_detail', args=[self.product.id]))
        self.assertEqual(response.status_code, 200)

    def test_about_page_status(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_page(self):
        response = self.client.get('/nonexistent/')
        self.assertEqual(response.status_code, 404)