from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from ..models import User

@login_required
def admin_dashboard_view(request):
    return render(request, 'dashboard/admin_dashboard.html')