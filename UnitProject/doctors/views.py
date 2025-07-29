from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from datetime import datetime, date

# Import models
from .models import Specialty, DoctorProfile, SimpleAppointment

# Doctor Dashboard View
def doctor_dashboard_view(request):
    doctor_id = request.GET.get('doctor_id') or request.POST.get('doctor_id')
    doctor_profile = None
    pending_appointments = None
    
    # Try to find doctor by ID
    if doctor_id:
        try:
            # Assuming doctor_id is the DoctorProfile.id
            doctor_profile = DoctorProfile.objects.get(id=doctor_id)
        except DoctorProfile.DoesNotExist:
            doctor_profile = None
    
    # If doctor found, get their pending appointments
    if doctor_profile:
        pending_appointments = SimpleAppointment.objects.filter(
            doctor=doctor_profile,
            status='pending'
        ).order_by('appointment_date', 'appointment_time')
    
    context = {
        'doctor_profile': doctor_profile,
        'pending_appointments': pending_appointments,
        'doctor_id': doctor_id,
    }
    return render(request, 'doctors/doctor_dashboard.html', context)

# Appointment Detail View for Doctor
def appointment_detail_view(request, appointment_id):
    # Get the appointment first
    appointment = get_object_or_404(SimpleAppointment, id=appointment_id)
    
    # Get doctor profile from the appointment
    doctor_profile = appointment.doctor
    
    context = {
        'appointment': appointment,
        'doctor_profile': doctor_profile,
    }
    return render(request, 'doctors/appointment_detail.html', context)

# Process Doctor Response
@require_POST
def process_doctor_response(request, appointment_id):
    # Get the appointment first
    appointment = get_object_or_404(SimpleAppointment, id=appointment_id)
    
    # Get doctor profile from the appointment
    doctor_profile = appointment.doctor
    
    doctor_response = request.POST.get('doctor_response', '').strip()
    
    if doctor_response:
        appointment.doctor_response = doctor_response
        appointment.response_date = datetime.now()
        appointment.status = 'completed'
        appointment.save()
        

        # Redirect back to dashboard with doctor email
        return redirect(f'/doctors/dashboard/?doctor_id={doctor_profile.id}')
    else:

        return redirect('doctors:appointment_detail_view', appointment_id=appointment_id)

# Doctor Profile View
def doctor_profile_view(request):
    # Get the first doctor profile for demo purposes
    doctor_profile = DoctorProfile.objects.first()
    if not doctor_profile:
        return redirect('main:home_view')
    
    if request.method == 'POST':
        # Handle profile update
        bio = request.POST.get('bio', '')
        consultation_fee = request.POST.get('consultation_fee', 0)
        
        try:
            doctor_profile.bio = bio
            doctor_profile.consultation_fee = float(consultation_fee) if consultation_fee else 0
            doctor_profile.save()
            
            return redirect('doctors:doctor_profile_view')
        except Exception as e:
            pass

    
    context = {
        'doctor_profile': doctor_profile,
        'specialties': Specialty.objects.all(),
    }
    return render(request, 'doctors/doctor_profile.html', context)

# Book Appointment View (Public)
def book_appointment_view(request, doctor_id):
    doctor_profile = get_object_or_404(DoctorProfile, id=doctor_id)
    
    if request.method == 'POST':
        # Get form data
        patient_name = request.POST.get('patient_name', '').strip()
        # patient_email = request.POST.get('patient_email', '').strip()
       # patient_phone = request.POST.get('patient_phone', '').strip()
        patient_id = request.POST.get('patient_id', '').strip()
        gender = request.POST.get('gender', '')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        health_condition = request.POST.get('health_condition', '').strip()
        appointment_date = request.POST.get('appointment_date')
      #  reason = request.POST.get('reason', '').strip()
        

        
        # Basic validation with specific error messages
        missing_fields = []
        if not patient_name:
            missing_fields.append("Full Name")
        if not patient_id:
            missing_fields.append("Patient ID")
        if not appointment_date:
            missing_fields.append("Appointment Date")
        
        if missing_fields:
            return render(request, 'doctors/book_appointment.html', {'doctor_profile': doctor_profile})
        

        
        try:
            # Create appointment with sequential time slots
            from datetime import datetime, time
            existing_appointments = SimpleAppointment.objects.filter(
                doctor=doctor_profile,
                appointment_date=appointment_date
            ).count()
            
            # Generate time slots starting from 9:00 AM
            base_hour = 9
            slot_minutes = existing_appointments * 30  # 30 minutes apart
            appointment_hour = base_hour + (slot_minutes // 60)
            appointment_minutes = slot_minutes % 60
            
            appointment_time = time(appointment_hour, appointment_minutes)
            
            appointment = SimpleAppointment.objects.create(
                doctor=doctor_profile,
                patient_name=patient_name,
                patient_email=patient_email or '',
                patient_phone=patient_phone or '',
                patient_id=patient_id,
                gender=gender,
                age=int(age) if age else None,
                height=float(height) if height else None,
                weight=float(weight) if weight else None,
                health_condition=health_condition,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason,
                status='pending'
            )
            

            return redirect('doctors:appointment_confirmation_view', appointment_id=appointment.id)
            
        except Exception as e:
            pass

    
    context = {
        'doctor_profile': doctor_profile,
    }
    return render(request, 'doctors/book_appointment.html', context)

# Appointment Confirmation View
def appointment_confirmation_view(request, appointment_id):
    appointment = get_object_or_404(SimpleAppointment, id=appointment_id)
    
    context = {
        'appointment': appointment,
    }
    return render(request, 'doctors/appointment_confirmation.html', context)
