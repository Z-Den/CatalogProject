from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        choices=[
            ('натуральный', 'Натуральный'),
            ('с добавлением консервантов', 'С добавлением консервантов'),
            ('диетический', 'Диетический')
        ],
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Product(models.Model):
    brand = models.CharField(max_length=100, verbose_name='Марка')
    flavor = models.CharField(max_length=100, verbose_name='Вкус')
    volume = models.FloatField(
        validators=[MinValueValidator(0.1)],
        verbose_name='Объем (л)'
    )
    sugar_content = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name='Содержание сахара (г/л)'
    )
    is_alcoholic = models.BooleanField(default=True, verbose_name='Алкогольный')
    expiration_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Срок годности'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name='Категория'
    )
    price = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за единицу'
    )
    small_wholesale_price = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена мелкий опт'
    )
    small_wholesale_quantity = models.PositiveIntegerField(
        default=10,
        verbose_name='Минимальное количество для мелкого опта'
    )
    large_wholesale_price = models.DecimalField(
        default=0,
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена крупный опт'
    )
    large_wholesale_quantity = models.PositiveIntegerField(
        default=50,
        verbose_name='Минимальное количество для крупного опта'
    )

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        permissions = [
            ("edit_product", "Может редактировать товары"),
        ]

    def __str__(self):
        return f"{self.brand} — {self.flavor}"

class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())

    def __str__(self):
        return f"Корзина {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Корзина'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(
        default=1,
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = "Позиция в корзине"
        verbose_name_plural = "Позиции в корзине"
        unique_together = ['cart', 'product']

    def unit_price(self):
        if self.quantity >= self.product.large_wholesale_quantity:
            return self.product.large_wholesale_price
        elif self.quantity >= self.product.small_wholesale_quantity:
            return self.product.small_wholesale_price
        return self.product.price

    def total_price(self):
        return self.unit_price() * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('confirmed', 'Подтвержден'),
        ('shipped', 'Отправлен'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен')
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Пользователь'
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_orders',
        verbose_name='Менеджер'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Статус'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Общая сумма'
    )
    discount = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Скидка (%)'
    )

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        permissions = [
            ("manage_order", "Может управлять заказами"),
        ]

    def calculate_total(self):
        subtotal = sum(item.total_price() for item in self.items.all())
        self.total_price = subtotal * (1 - self.discount / 100)
        self.save()

    def __str__(self):
        return f"Заказ #{self.id} - {self.get_status_display()}"

class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Заказ'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        verbose_name='Товар'
    )
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена за единицу'
    )

    class Meta:
        verbose_name = "Позиция заказа"
        verbose_name_plural = "Позиции заказов"

    def total_price(self):
        return self.unit_price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product} @ {self.unit_price}"
