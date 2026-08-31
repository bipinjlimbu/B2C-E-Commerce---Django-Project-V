from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product, Wishlist

@login_required
def wishlist_toggle_view(request, product_id):
    if not request.user.is_authenticated and request.user.is_superuser:
        messages.error(request, 'You are not authorized to add products to the wishlist.')
        return redirect('/')
    
    product = Product.objects.get(id=product_id)
    
    if not product:
        messages.error(request, 'Product does not exist.')
        return redirect('/products/')
    
    if Wishlist.objects.filter(customer=request.user, product=product).exists():
        wishlist_item = Wishlist.objects.get(customer=request.user, product=product)
        wishlist_item.delete()
        messages.success(request, 'Product removed from wishlist.')
    else:
        Wishlist.objects.create(customer=request.user, product=product)
        messages.success(request, 'Product added to wishlist.')
        
    return redirect(f'/products/{product_id}/')

