from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Product, Brand

@login_required
def add_product_view(request):
    errors = {}
    brands = Brand.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name')
        brand_id = request.POST.get('brand')
        category = request.POST.get('category')
        skin_type = request.POST.get('skin_type')
        volume = request.POST.get('volume')
        ingredients = request.POST.get('ingredients')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        sku = request.POST.get('sku')
        product_image = request.FILES.get('product_image')
        is_active = request.POST.get('is_active') == 'true'

        if not name:
            errors['name'] = 'Product name is required.'
        if not brand_id:
            errors['brand'] = 'Brand is required.'
        if not category:
            errors['category'] = 'Category is required.'
        if not volume:
            errors['volume'] = 'Volume is required.'
        if not description:
            errors['description'] = 'Description is required.'
        if not price:
            errors['price'] = 'Price is required.'
        if not stock:
            errors['stock'] = 'Stock is required.'
            
        if not sku:
            errors['sku'] = 'SKU is required.'
        elif Product.objects.filter(sku=sku).exists():
            errors['sku'] = 'SKU already exists.'
            
        if not product_image:
            errors['product_image'] = 'Product image is required.'

        if errors:
            return render(request, 'main/add_product_page.html', {'data':request.POST,'errors': errors,'brands': brands})

        brand = Brand.objects.get(id=brand_id)
        product = Product(
            name=name,
            brand=brand,
            category=category,
            skin_type=skin_type,
            volume=volume,
            ingredients=ingredients,
            description=description,
            price=price,
            stock=stock,
            sku=sku,
            product_image=product_image,
            is_active=is_active
        )
        product.save()
        messages.success(request, 'Product added successfully.')
        return redirect('/dashboard/admin/?section=product-management')
    
    return render(request, 'main/add_product_page.html', {'brands': brands})

@login_required
def edit_product_view(request, product_id):
    return render(request, 'main/edit_product_page.html', {'product_id': product_id})