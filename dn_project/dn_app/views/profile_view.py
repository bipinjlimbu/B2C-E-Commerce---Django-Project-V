from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import User

@login_required
def profile_view(request):
    return render(request, 'main/profile_page.html', {'user': request.user})

@login_required
def edit_profile_view(request):
    errors = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        profile_picture = request.FILES.get('profile_picture')

        if not username:
            errors['username'] = 'Username is required.'
        elif User.objects.filter(username=username).exclude(id=request.user.id).exists():
            errors['username'] = 'Username already exists.'
            
        if not email:
            errors['email'] = 'Email is required.'
        elif User.objects.filter(email=email).exclude(id=request.user.id).exists():
            errors['email'] = 'Email already exists.'

        if errors:
            return render(request, 'main/edit_profile_page.html', {'data':request.POST,'errors': errors})

        user = User.objects.get(id=request.user.id)
        user.username = username
        user.email = email
        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone
        user.address = address
        if profile_picture:
            user.profile_picture = profile_picture
        user.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('/profile/')
    
    return render(request, 'main/edit_profile_page.html')

@login_required
def delete_profile_view(request, profile_id):
    if request.user.id != profile_id and not request.user.is_superuser:
        messages.error(request, 'You are not authorized to delete this profile.')
        return redirect('/profile/')
    
    try:
        user = User.objects.get(id=profile_id)
        user.delete()
        messages.success(request, 'Profile deleted successfully.')
        
        if request.user.id == profile_id:
            return redirect('/')
        else:
            return redirect('/dashboard/admin/?section=customer-management')
        
    except User.DoesNotExist:
        messages.error(request, 'Profile does not exist.')
        return redirect('/profile/')