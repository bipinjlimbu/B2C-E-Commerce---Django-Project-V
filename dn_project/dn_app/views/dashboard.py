from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def admin_dashboard_view(request):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to access the admin dashboard.')
        return redirect('/')
    
    section = request.GET.get('section', 'customer-management')
    
    context = {
        'section': section,
    }
    
    if section == 'customer-management':
        context['customers'] = None
    
    if section == 'product-management':
        context['products'] = None

    if section == 'brand-management':
        context['brands'] = None

    if section == 'order-fulfillment':
        context['orders'] = None
    
    if section == 'product-reviews':
        context['reviews'] = None
        
    if section == 'revenue-logs':
        context['logs'] = None
    
    return render(request, 'dashboard/admin_dashboard.html', context)

@login_required
def customer_dashboard_view(request):
    return render(request, 'dashboard/customer_dashboard.html', {'user': request.user})