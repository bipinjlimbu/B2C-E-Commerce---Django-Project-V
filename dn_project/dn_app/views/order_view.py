from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Order

@login_required
def dispatch_order_view(request, order_id):
    if not request.user.is_superuser:
        messages.error(request, 'You are not authorized to access this page.')
        return redirect('/')
    
    order = Order.objects.get(id=order_id)
    if not order:
        messages.error(request, 'Order does not exist.')
        return redirect('/dashboard/admin/?section=order-fulfillment')
    
    if order.status != Order.Status.CONFIRMED:
        messages.error(request, 'Only confirmed orders can be dispatched.')
        return redirect('/dashboard/admin/?section=order-fulfillment')
    
    order.status = Order.Status.SHIPPING
    order.save()
    messages.success(request, 'Order dispatched successfully.')
    return redirect('/dashboard/admin/?section=order-fulfillment')