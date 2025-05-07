from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
from django.contrib import messages
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import AddToCartForm, OrderForm, ProductForm

@permission_required('catalog.add_product', raise_exception=True)
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # или куда тебе нужно
    else:
        form = ProductForm()
    return render(request, 'product_create.html', {'form': form})

def product_list(request):
    products = Product.objects.all()
    
    # Фильтрация для гостей
    if not request.user.is_authenticated: # or not request.user.has_perm('catalog.view_product'):
        products = products.filter(is_alcoholic=False)
    
    # Поиск
    query = request.GET.get('search')
    if query:
        products = products.filter(
            Q(brand__icontains=query) | Q(flavor__icontains=query))
    
    # Фильтрация по категории
    category = request.GET.get('category')
    if category:
        products = products.filter(category__name=category)
    
    # Сортировка
    sort_by = request.GET.get('sort')
    if sort_by in ['brand', 'price', 'sugar_content']:
        products = products.order_by(sort_by)
    
    categories = Category.objects.all()
    return render(request, 'product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'selected_category': category,
        'selected_sort': sort_by,
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Проверка прав доступа
    if product.is_alcoholic and not request.user.has_perm('catalog.view_product'):
        return render(request, 'access_denied.html', status=403)
    
    form = AddToCartForm() if request.user.is_authenticated else None

    return render(request, 'product_detail.html', {
        'product': product,
        'form': form
    })

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': quantity}
            )
            
            if not created:
                cart_item.quantity += quantity
                cart_item.save()
            
            messages.success(request, f"{product} добавлен в корзину")
            return redirect('cart_detail')
    
    return redirect('product_detail', pk=product.id)

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)
    return render(request, 'cart_detail.html', {'cart': cart})

@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        if quantity > 0:
            cart_item.quantity = quantity
            cart_item.save()
        else:
            cart_item.delete()
    
    return redirect('cart_detail')

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect('cart_detail')

@login_required
@permission_required('catalog.manage_order', raise_exception=True)
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.manager = request.user
            order.save()
            
            # Переносим товары из корзины в заказ
            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    unit_price=item.unit_price()
                )
            
            # Рассчитываем итоговую сумму
            order.calculate_total()
            
            # Очищаем корзину
            cart.items.all().delete()
            
            messages.success(request, "Заказ успешно создан")
            return redirect('order_detail', pk=order.id)
    else:
        form = OrderForm()
    
    return render(request, 'create_order.html', {
        'form': form,
        'cart': cart
    })

@login_required
def order_list(request):
    if request.user.has_perm('catalog.manage_order'):
        orders = Order.objects.all()
    else:
        orders = Order.objects.filter(user=request.user)
    
    return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, pk):
    if request.user.has_perm('catalog.manage_order'):
        order = get_object_or_404(Order, pk=pk)
    else:
        order = get_object_or_404(Order, pk=pk, user=request.user)
    
    return render(request, 'order_detail.html', {'order': order})

@login_required
@permission_required('catalog.manage_order', raise_exception=True)
def update_order_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk)
    
    if status in [choice[0] for choice in Order.STATUS_CHOICES]:
        order.status = status
        order.save()
        messages.success(request, f"Статус заказа изменен на {order.get_status_display()}")
    
    return redirect('order_detail', pk=order.id)

@login_required
@permission_required('catalog.change_product', raise_exception=True)
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_edit.html', {'form': form, 'product': product})


def about(request):
    return render(request, 'about.html')

# from django.shortcuts import render, get_object_or_404
# from .models import Product, Category
# from django.db.models import Q

# def product_list(request):
#     products = Product.objects.all()

#     # Поиск
#     query = request.GET.get('search')
#     if query:
#         products = products.filter(
#             Q(brand__icontains=query) | Q(flavor__icontains=query)
#         )

#     # Фильтрация по категории
#     category = request.GET.get('category')
#     if category:
#         products = products.filter(category__name=category)

#     # Сортировка
#     sort_by = request.GET.get('sort')
#     if sort_by in ['brand', 'sugar_content', 'expiration_date']:
#         products = products.order_by(sort_by)

#     categories = Category.objects.all()
#     return render(request, 'catalog/product_list.html', {
#         'products': products,
#         'categories': categories,
#         'query': query,
#         'selected_category': category,
#         'selected_sort': sort_by,
#     })

# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     return render(request, 'catalog/product_detail.html', {'product': product})

# def about(request):
#     return render(request, 'catalog/about.html')
