from django.test import TestCase
from django.urls import reverse
from catalog.models import Product, Category

class ContentTests(TestCase):
    def setUp(self):
        # Создаем и сохраняем категории
        self.category1 = Category.objects.create(name='натуральный')
        self.category2 = Category.objects.create(name='диетический')
        
        # Создаем и сохраняем продукты
        self.product1 = Product.objects.create(
            brand="AAA Brand",
            sugar_content=5,
            volume=0.5,
            is_alcoholic=False,
            flavor="Ягодный",
            category=self.category1
        )
        self.product2 = Product.objects.create(
            brand="BBB Brand",
            sugar_content=15,
            volume=1,
            is_alcoholic=True,
            flavor="Цитрусовый",
            category=self.category2
        )

    def test_product_list_content(self):
        response = self.client.get(reverse('product_list'))
        self.assertContains(response, self.product1.brand)
        self.assertContains(response, self.product2.brand)

    def test_product_detail_content(self):
        response = self.client.get(reverse('product_detail', args=[self.product1.id]))
        self.assertContains(response, self.product1.brand)
        self.assertContains(response, str(self.product1.sugar_content))

    def test_about_page_content(self):
        response = self.client.get(reverse('about'))
        self.assertContains(response, "натуральные морсы")

    def test_filtering(self):
        response = self.client.get(f"{reverse('product_list')}?category=натуральный")
        self.assertContains(response, self.product1.brand)
        self.assertNotContains(response, self.product2.brand)

    def test_sorting(self):
        response = self.client.get(f"{reverse('product_list')}?sort=brand")
        content = response.content.decode()
        pos1 = content.find(self.product1.brand)
        pos2 = content.find(self.product2.brand)
        self.assertTrue(pos1 != -1 and pos2 != -1 and pos1 < pos2)