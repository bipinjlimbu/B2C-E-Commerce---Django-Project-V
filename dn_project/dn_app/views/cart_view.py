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