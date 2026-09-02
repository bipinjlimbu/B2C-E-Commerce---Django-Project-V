from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import Review, Product

@login_required
def add_review_view(request, product_id):
    if request.user.is_superuser:
        messages.error(request, 'Admins cannot add reviews.')
        return redirect('products')
    
    product = Product.objects.filter(id=product_id).first()
    
    if not product:
        messages.error(request, 'Product not found.')
        return redirect('products')
    
    errors = {}
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating:
            errors['rating'] = 'Rating is required.'
        elif not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            errors['rating'] = 'Rating must be an integer between 1 and 5.'

        if not comment:
            errors['comment'] = 'Comment is required.'

        if errors:
            return render(request, 'main/add_review_page.html', {'product': product, 'errors': errors, 'data': request.POST})

        review = Review(product=product, customer=request.user, rating=int(rating), comment=comment)
        review.save()
        messages.success(request, 'Review added successfully.')
        return redirect('product_detail', product_id=product_id)
    
    return render(request, 'main/add_review_page.html', {'product': product})

@login_required
def edit_review_view(request, review_id):
    if request.user.is_superuser:
        messages.error(request, 'Admins cannot edit reviews.')
        return redirect('products')
    
    review = Review.objects.filter(id=review_id, customer=request.user).first()
    
    if not review:
        messages.error(request, 'Review not found or you are not authorized to edit this review.')
        return redirect('products')
    
    if review.customer != request.user:
        messages.error(request, 'You are not authorized to edit this review.')
        return redirect('products')
    
    errors = {}
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')

        if not rating:
            errors['rating'] = 'Rating is required.'
        elif not rating.isdigit() or int(rating) < 1 or int(rating) > 5:
            errors['rating'] = 'Rating must be an integer between 1 and 5.'

        if not comment:
            errors['comment'] = 'Comment is required.'

        if errors:
            return render(request, 'main/edit_review_page.html', {'review': review, 'errors': errors, 'data': request.POST})

        review.rating = int(rating)
        review.comment = comment
        review.save()
        messages.success(request, 'Review updated successfully.')
        return redirect('/dashboard/?section=my-reviews')
    
    return render(request, 'main/edit_review_page.html', {'review': review})