from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
from datetime import datetime, date

# Import models
from .models import Specialty, DoctorProfile, SimpleAppointment, Appointment, Consultation, DoctorAvailability

# Doctor Dashboard View
def doctor_dashboard_view(request):
    doctor_email = request.GET.get('doctor_email') or request.POST.get('doctor_email')
    doctor_profile = None
    today_appointments = []
    upcoming_appointments = []
    pending_appointments = []
    completed_appointments_count = 0
    
    if doctor_email:
        # Find doctor by email
        try:
            doctor_user = User.objects.get(email=doctor_email)
            doctor_profile = DoctorProfile.objects.get(user=doctor_user)
            
            # Get today's appointments from SimpleAppointment
            today_appointments = SimpleAppointment.objects.filter(
                doctor=doctor_profile,
                appointment_date=date.today()
            ).order_by('appointment_time')
            
            # Get upcoming appointments
            upcoming_appointments = SimpleAppointment.objects.filter(
                doctor=doctor_profile,
                appointment_date__gt=date.today()
            ).order_by('appointment_date', 'appointment_time')[:5]
            
            # Get pending appointments (need doctor response)
            pending_appointments = SimpleAppointment.objects.filter(
                doctor=doctor_profile,
                status='pending'
            ).order_by('appointment_date', 'appointment_time')
            
            # Get completed appointments count
            completed_appointments_count = SimpleAppointment.objects.filter(
                doctor=doctor_profile,
                status='completed'
            ).count()
            
        except (User.DoesNotExist, DoctorProfile.DoesNotExist):
            messages.error(request, 'Doctor not found with this email address')
    
    context = {
        'doctor_profile': doctor_profile,
        'doctor_email': doctor_email,
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'pending_appointments': pending_appointments,
        'completed_appointments_count': completed_appointments_count,
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
        'doctor_email': doctor_profile.user.email,
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
        
        messages.success(request, f'Response sent successfully to {appointment.patient_name}! Appointment marked as completed.')
        # Redirect back to dashboard with doctor email
        return redirect(f'/doctors/dashboard/?doctor_email={doctor_profile.user.email}')
    else:
        messages.error(request, 'Please provide a response before submitting.')
        return redirect('doctors:appointment_detail_view', appointment_id=appointment_id)

# Doctor Profile View
def doctor_profile_view(request):
    # Get the first doctor profile for demo purposes
    doctor_profile = DoctorProfile.objects.first()
    if not doctor_profile:
        messages.error(request, 'No doctor profiles found')
        return redirect('main:home_view')

            
            messages.success(request, 'Profile updated successfully!')
            return redirect('doctors:doctor_profile_view')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
    
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
        patient_email = request.POST.get('patient_email', '').strip()
        patient_phone = request.POST.get('patient_phone', '').strip()
        patient_id = request.POST.get('patient_id', '').strip()
        gender = request.POST.get('gender', '')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        health_condition = request.POST.get('health_condition', '').strip()
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason', '').strip()
        health_document = request.FILES.get('health_document')
        

    
        
        if missing_fields:
            if len(missing_fields) == 1:
                messages.error(request, f'Please fill in the {missing_fields[0]} field.')
            else:
                messages.error(request, f'Please fill in the following required fields: {", ".join(missing_fields)}.')
            return render(request, 'doctors/book_appointment.html', {'doctor_profile': doctor_profile})
        
        # Email validation
        import re
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, patient_email):
            messages.error(request, 'Please enter a valid email address.')
            return render(request, 'doctors/book_appointment.html', {'doctor_profile': doctor_profile})
        
        try:
            # Create appointment
            appointment = SimpleAppointment.objects.create(
                doctor=doctor_profile,
                patient_name=patient_name,
                patient_id=patient_id,
                gender=gender,
                age=int(age) if age else None,
                height=float(height) if height else None,
                weight=float(weight) if weight else None,
                health_condition=health_condition
                reason=reason,
                health_document=health_document,
                status='pending'
            )
            
            messages.success(request, f'Appointment booked successfully! Your appointment ID is {appointment.id}')
            return redirect('doctors:appointment_confirmation_view', appointment_id=appointment.id)
            
        except Exception as e:
            messages.error(request, f'Error booking appointment: {str(e)}')
    
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
