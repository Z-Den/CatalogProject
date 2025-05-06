from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.db.models import Q

def product_list(request):
    products = Product.objects.all()

    # Поиск
    query = request.GET.get('search')
    if query:
        products = products.filter(
            Q(brand__icontains=query) | Q(flavor__icontains=query)
        )

    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        products = products.filter(category__name=category)

    # Сортировка
    sort_by = request.GET.get('sort')
    if sort_by in ['brand', 'sugar_content', 'expiration_date']:
        products = products.order_by(sort_by)

    categories = Category.objects.all()
    return render(request, 'catalog/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category,
        'selected_sort': sort_by,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'catalog/product_detail.html', {'product': product})

def about(request):
    return render(request, 'catalog/about.html')
