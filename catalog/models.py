from django.db import models
from django.core.validators import MinValueValidator


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
    sugar_content = models.FloatField(
        validators=[MinValueValidator(0)],
        verbose_name='Содержание сахара (г/л)'
    )
    volume = models.FloatField(
        validators=[MinValueValidator(0.1)],
        verbose_name='Объем (л)'
    )
    is_alcoholic = models.BooleanField(default=True, verbose_name='Алкогольный')
    flavor = models.CharField(max_length=100, verbose_name='Вкус')
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

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return f"{self.brand} — {self.flavor}"
