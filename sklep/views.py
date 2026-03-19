from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, F
from .models import Product, Order, OrderItem
from .forms import ProductForm, OrderForm, OrderItemFormSet

def dashboard(request):
    total_products = Product.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    total_revenue = Order.objects.filter(status='Completed').aggregate(total=Sum('total_price'))['total']
    
    out_of_stock = Product.objects.filter(stock=0)[:5]
    recent_orders = Order.objects.all().order_by('-created_at')[:5]

    context = {
        'total_products': total_products,
        'pending_orders': pending_orders,
        'total_revenue': total_revenue,
        'out_of_stock': out_of_stock,
        'recent_orders': recent_orders,
    }
    return render(request, 'sklep/dashboard.html', context)

# --- Product Views ---
def product_list(request):
    products = Product.objects.all().select_related('category')
    return render(request, 'sklep/product_list.html', {'products': products})

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Produkt "{product.name}" został pomyślnie dodany.')
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'sklep/product_form.html', {'form': form})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            product = form.save()
            messages.success(request, f'Produkt "{product.name}" został zaktualizowany.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'sklep/product_form.html', {'form': form, 'product': product})

def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        name = product.name
        product.delete()
        messages.success(request, f'Produkt "{name}" został usunięty.')
        return redirect('product_list')
    return render(request, 'sklep/product_confirm_delete.html', {'product': product})

# --- Order Views ---
def order_list(request):
    orders = Order.objects.all().order_by('-created_at').prefetch_related('items__product')
    return render(request, 'sklep/order_list.html', {'orders': orders})

def order_create(request):
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        formset = OrderItemFormSet(request.POST)
        
        if order_form.is_valid() and formset.is_valid():
            order = order_form.save()
            items = formset.save(commit=False)
            
            total_price = 0
            for item in items:
                item.order = order
                # Decrease product stock
                item.product.stock -= item.quantity
                item.product.save()
                
                # Calculate price
                item.unit_price = item.product.price
                total_price += item.quantity * item.unit_price
                item.save()
            
            # Save total price to order
            order.total_price = total_price
            order.save()
            
            messages.success(request, f'Zamówienie #{order.id} zostało złożone.')
            return redirect('order_list')
    else:
        order_form = OrderForm()
        formset = OrderItemFormSet()
        
    context = {
        'order_form': order_form,
        'formset': formset,
    }
    return render(request, 'sklep/order_form.html', context)
