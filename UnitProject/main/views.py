from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
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



def doctors_list_view(request):
    """List all doctors with filtering options"""
    doctors = DoctorProfile.objects.select_related('user', 'specialty').all()
    specialties = Specialty.objects.all()
    
    # Get filter parameters
    specialty_filter = request.GET.get('specialty')
    gender_filter = request.GET.get('gender')
    search_query = request.GET.get('search')
    
    # Apply filters
    if specialty_filter:
        doctors = doctors.filter(specialty_id=specialty_filter)
    
    if gender_filter:
        doctors = doctors.filter(gender=gender_filter)
    
    if search_query:
        doctors = doctors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
    
    # Gender choices for the filter dropdown
    gender_choices = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    context = {
        'doctors': doctors,
        'specialties': specialties,
        'selected_specialty': int(specialty_filter) if specialty_filter else None,
        'selected_gender': gender_filter,
        'gender_choices': gender_choices,
        'search_query': search_query,
    }
    return render(request, 'main/doctors_list.html', context)