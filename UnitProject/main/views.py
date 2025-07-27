from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime, date

# Import models from different apps
from doctors.models import Specialty, DoctorProfile, SimpleAppointment

# Public Views
def home_view(request):
    """Main home page"""
    context = {
        'specialties': Specialty.objects.all()[:4],  # Show first 4 specialties
        'doctors_count': DoctorProfile.objects.count(),
        'recent_appointments': SimpleAppointment.objects.count(),
    }
    return render(request, 'main/home.html', context)

def about_view(request):
    """About page"""
    return render(request, 'main/about.html')

def contact_view(request):
    """Contact page"""
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Here you can add logic to save contact form or send email
        # For now, just show a success message
        messages.success(request, f'Thank you {name}! Your message has been sent successfully.')
        return redirect('main:contact_view')
    
    return render(request, 'main/contact.html')

def doctors_list_view(request):
    """List all doctors with filtering options"""
    doctors = DoctorProfile.objects.select_related('user', 'specialty').all()
    specialties = Specialty.objects.all()
    
    # Filter by specialty if provided
    specialty_filter = request.GET.get('specialty')
    if specialty_filter:
        doctors = doctors.filter(specialty_id=specialty_filter)
    
    # Search by name if provided
    search_query = request.GET.get('search')
    if search_query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    context = {
        'doctors': doctors,
        'specialties': specialties,
        'selected_specialty': int(specialty_filter) if specialty_filter else None,
        'search_query': search_query,
    }
    return render(request, 'main/doctors_list.html', context)

#
    return render(request, 'main/my_appointments.html', context)
