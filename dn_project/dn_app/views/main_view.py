from django.shortcuts import render
from ..models import Product, Brand

def home_view(request):
    context = {
        'products': Product.objects.filter(is_active=True),
        'brands': Brand.objects.all(),
    }       
    return render(request, 'main/home_page.html', context)