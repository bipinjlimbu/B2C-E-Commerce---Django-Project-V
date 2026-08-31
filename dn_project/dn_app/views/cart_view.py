from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Cart, CartItem, Product

@login_required
def add_to_cart_view(request, product_id):
    if not request.user.is_authenticated and request.user.is_superuser:
        messages.error(request, 'You are not authorized to add products to the cart.')
        return redirect('/')
    
    product = Product.objects.get(id=product_id)
    
    if not product:
        messages.error(request, 'Product does not exist.')
        return redirect('/products/')
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    
    if CartItem.objects.filter(cart=cart, product=product).exists():
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, 'Product quantity updated in the cart.')
    else:
        CartItem.objects.create(cart=cart, product=product, quantity=1)
        messages.success(request, 'Product added to the cart.')
        
    return redirect(f'/products/{product_id}/')

@login_required
def cart_view(request):
    if not request.user.is_authenticated and request.user.is_superuser:
        messages.error(request, 'You are not authorized to view the cart.')
        return redirect('/')
    
    cart, created = Cart.objects.get_or_create(customer=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    return render(request, 'main/cart_page.html', {'cart_items': cart_items, 'total_price': total_price})

@login_required
def increase_cart_item_quantity_view(request, cart_item_id):
    if not request.user.is_authenticated and request.user.is_superuser:
        messages.error(request, 'You are not authorized to modify the cart.')
        return redirect('/')
    
    cart_item = CartItem.objects.get(id=cart_item_id)
    
    if not cart_item:
        messages.error(request, 'Cart item does not exist.')
        return redirect('/cart/')
    
    if cart_item.cart.customer != request.user:
        messages.error(request, 'You are not authorized to modify this cart item.')
        return redirect('/cart/')
    
    if cart_item.quantity >= cart_item.product.stock:
        messages.error(request, 'Cannot increase quantity. Not enough stock available.')
        return redirect('/cart/')
    
    cart_item.quantity += 1
    cart_item.save()
    messages.success(request, 'Product quantity increased in the cart.')
        
    return redirect('/cart/')

@login_required
def decrease_cart_item_quantity_view(request, cart_item_id):
    if not request.user.is_authenticated and request.user.is_superuser:
        messages.error(request, 'You are not authorized to modify the cart.')
        return redirect('/')
    
    cart_item = CartItem.objects.get(id=cart_item_id)
    
    if not cart_item:
        messages.error(request, 'Cart item does not exist.')
        return redirect('/cart/')
    
    if cart_item.cart.customer != request.user:
        messages.error(request, 'You are not authorized to modify this cart item.')
        return redirect('/cart/')
    
    if cart_item.quantity <= 1:
        messages.error(request, 'Cannot decrease quantity below 1. Remove the item from the cart instead.')
        return redirect('/cart/')
    
    cart_item.quantity -= 1
    cart_item.save()
    messages.success(request, 'Product quantity decreased in the cart.')
        
    return redirect('/cart/')