from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User, Brand, Product, Order, OrderItem

@login_required
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to access the admin dashboard.')
        return redirect('/')
    
    section = request.GET.get('section', 'customer-management')
    
    context = {
        'section': section,
        'awaiting_dispatch_count': Order.objects.filter(status=Order.Status.CONFIRMED).count(),
        'awaiting_delivery_count': Order.objects.filter(status=Order.Status.SHIPPING).count(),
        'delivered_count': Order.objects.filter(status=Order.Status.DELIVERED).count(),
        'completed_count': Order.objects.filter(status=Order.Status.COMPLETED).count(),
        'cancelled_count': Order.objects.filter(status=Order.Status.CANCELLED).count(),
    }
    
    if section == 'customer-management':
        context['customers'] = User.objects.filter(is_superuser=False)
    
    if section == 'product-management':
        context['products'] = Product.objects.all()

    if section == 'brand-management':
        context['brands'] = Brand.objects.all()

    if section == 'order-fulfillment':
        context['orders'] = Order.objects.all().order_by('-created_at')
    
    if section == 'product-reviews':
        context['reviews'] = None
        
    if section == 'revenue-logs':
        context['logs'] = None
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def customer_dashboard_view(request):
    if request.user.is_superuser:
        messages.error(request, 'Superusers cannot access the customer dashboard.')
        return redirect('/dashboard/admin/')
    
    section = request.GET.get('section', 'pending-orders')
    
    context = {
        'section': section,
    }
    
    if section == 'pending-orders':
        context['pending_orders'] = Order.objects.filter(customer=request.user).exclude(status__in=[Order.Status.COMPLETED, Order.Status.CANCELLED]).order_by('-created_at')
        
    if section == 'my-orders':
        context['my_orders'] = None
        
    if section == 'total-spent':
        context['total_spent'] = None
        
    if section == 'my-reviews':
        context['my_reviews'] = None

    return render(request, 'dashboard/customer_dashboard.html', context)