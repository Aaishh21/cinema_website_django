from django.shortcuts import render, HttpResponseRedirect, redirect
from users.forms import UserLoginForm, UserRegisterForm
from django.contrib import messages
from django.contrib import auth
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from tickets.models import Booking

User = get_user_model()

@login_required(login_url='users:login')
def profile(request):
    if request.method == 'POST':
        user = request.user
        is_avatar_only = 'avatar' in request.FILES and 'full_name' not in request.POST and 'phone_number' not in request.POST and 'email' not in request.POST
        
        if 'full_name' in request.POST:
            user.full_name = request.POST.get('full_name')
        if 'email' in request.POST:
            user.email = request.POST.get('email')
        if 'phone_number' in request.POST:
            user.phone_number = request.POST.get('phone_number')
        if 'avatar' in request.FILES:
            user.avatar = request.FILES['avatar']
        user.save()
        
        if is_avatar_only:
            return JsonResponse({'status': 'success', 'message': 'Avatar updated successfully!'})
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('users:profile')
    
    user_bookings = Booking.objects.filter(user=request.user).select_related('showtime__movie', 'showtime__hall')
    now = timezone.now()
    
    active_orders = user_bookings.filter(showtime__start_time__gte=now).order_by('showtime__start_time')
    past_orders = user_bookings.filter(showtime__start_time__lt=now).order_by('-showtime__start_time')
    
    context = {
        'active_orders': active_orders,
        'past_orders': past_orders,
    }
    
    return render(request, 'users/profile.html', context)

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user = User.objects.get(email=email)
                if user.check_password(password):
                    auth.login(request, user)
                    return redirect('movies:homepage')
                else:
                    form.add_error(None, 'Invalid email or password.')
            except User.DoesNotExist:
                form.add_error(None, 'Invalid email or password.')
    else:
        form = UserLoginForm()
    context = {'form': form}
    return render(request, 'users/login.html', context)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Registration successful! Please log in.')
                return HttpResponseRedirect(reverse('users:login'))
            except Exception as e:
                form.add_error(None, f'Registration failed: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = UserRegisterForm()
    context = {'form': form}
    return render(request, 'users/register.html', context)

def logout(request):
    auth.logout(request)
    return redirect('movies:homepage')