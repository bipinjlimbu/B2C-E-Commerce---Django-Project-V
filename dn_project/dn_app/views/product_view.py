from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from ..models import Product, Brand

def products_view(request):
    brands = Brand.objects.all()
    products = Product.objects.filter(is_active=True)
    
    category = request.GET.get('category', 'all')
    skin_type = request.GET.get('skin_type', 'any')
    brand_id = request.GET.get('brand', 'all')
    price_range = request.GET.get('price_range', 'all')
    sort = request.GET.get('sort', 'latest')
    search = request.GET.get('search', '').strip()
    
    if category != 'all':
        products = products.filter(category=category)
        
    if skin_type != 'any':
        products = products.filter(skin_type=skin_type)
        
    if brand_id != 'all':
        products = products.filter(brand__id=brand_id)
        
    if price_range != 'all':
        if price_range == '0-999':
            products = products.filter(price__lt=1000)
        elif price_range == '1000-4999':
            products = products.filter(price__gte=1000, price__lt=5000)
        elif price_range == '5000-9999':
            products = products.filter(price__gte=5000, price__lt=10000)
        elif price_range == '10000-49999':
            products = products.filter(price__gte=10000, price__lt=50000)
        elif price_range == '50000+':
            products = products.filter(price__gte=50000)
            
    if sort:
        if sort == 'latest':
            products = products.order_by('-created_at')
        elif sort == 'price_asc':
            products = products.order_by('price')
        elif sort == 'price_desc':
            products = products.order_by('-price')
        elif sort == 'stock_asc':
            products = products.order_by('stock')
        elif sort == 'stock_desc':
            products = products.order_by('-stock')
            
    if search:
        products = products.filter(Q(name__icontains=search) | Q(brand__name__icontains=search) | Q(ingredients__icontains=search) | Q(description__icontains=search))
        
    return render(request, 'main/products_page.html', {'products': products, 'brands': brands})

@login_required
def add_product_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to add a product.')
        return redirect('/')
    
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
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to edit this product.')
        return redirect('/')
    
    product = Product.objects.get(id=product_id)
    brands = Brand.objects.all()
    
    if not product:
        messages.error(request, 'Product does not exist.')
        return redirect('/dashboard/admin/?section=product-management')
    
    errors = {}
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
        elif Product.objects.filter(sku=sku).exclude(id=product_id).exists():
            errors['sku'] = 'SKU already exists.'

        if errors:
            return render(request, 'main/edit_product_page.html', {'product': product, 'data':request.POST,'errors': errors,'brands': brands})

        brand = Brand.objects.get(id=brand_id)
        
        product.name = name
        product.brand = brand
        product.category = category
        product.skin_type = skin_type
        product.volume = volume
        product.ingredients = ingredients
        product.description = description
        product.price = price
        product.stock = stock
        product.sku = sku
        if product_image:
            product.product_image = product_image
        product.is_active = is_active
        
        product.save()
        messages.success(request, 'Product updated successfully.')
        return redirect('/dashboard/admin/?section=product-management')
    
    return render(request, 'main/edit_product_page.html', {'product': product, 'brands': brands})

@login_required
def product_toggle_status_view(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to change the status of this product.')
        return redirect('/')
    
    product = Product.objects.get(id=product_id)
    
    if not product:
        messages.error(request, 'Product does not exist.')
        return redirect('/dashboard/admin/?section=product-management')
    
    product.is_active = not product.is_active
    product.save()
    status = 'activated' if product.is_active else 'deactivated'
    messages.success(request, f'Product {status} successfully.')
    return redirect('/dashboard/admin/?section=product-management')

@login_required
def delete_product_view(request, product_id):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to delete this product.')
        return redirect('/')
    
    product = Product.objects.get(id=product_id)
    
    if not product:
        messages.error(request, 'Product does not exist.')
        return redirect('/dashboard/admin/?section=product-management')

    product.delete()
    messages.success(request, 'Product deleted successfully.')
    return redirect('/dashboard/admin/?section=product-management')

def product_detail_view(request, product_id):
    product = Product.objects.get(id=product_id)
    
    if not product:
        messages.error(request, 'Product does not exist.')
        return redirect('/products/')

    return render(request, 'main/product_detail_page.html', {'product': product})