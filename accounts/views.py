
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import RegistrationForm

# Homepage
def home(request):
    return render(request, 'accounts/home.html')

# Student registration
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})

# User login
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form})

# Main dashboard redirect
@login_required
def dashboard(request):
    if request.user.is_superuser or request.user.role == 'admin':
        return redirect('admin_dashboard')
    elif request.user.role == 'teacher':
        return redirect('teacher_dashboard')
    else:
        return redirect('student_dashboard')

# Admin dashboard
@login_required
def admin_dashboard(request):
    if not (request.user.is_superuser or request.user.role == 'admin'):
        return redirect('dashboard')

    return render(request, 'admin/dashboard.html')

# Teacher dashboard
@login_required
def teacher_dashboard(request):
    if request.user.role != 'teacher':
        return redirect('dashboard')

    return render(request, 'teachers/dashboard.html')

# Student dashboard
@login_required
def student_dashboard(request):
    if request.user.role != 'student':
        return redirect('dashboard')

    return render(request, 'students/dashboard.html')

# Logout
def user_logout(request):
    logout(request)
    return redirect('login')