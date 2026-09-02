from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Review

@login_required
def add_review_view(request, product_id):
    return render(request, 'main/add_review_page.html', {'product_id': product_id})