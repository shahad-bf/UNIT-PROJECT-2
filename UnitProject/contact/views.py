from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from .models import Specialty, DoctorProfile, PatientProfile, Appointment, Consultation, DoctorAvailability, PatientMedicalRecord, SimpleAppointment
from django.views.decorators.http import require_POST
from datetime import datetime, date

# Home view
def home_view(request):
    return render(request, "main/home.html")

# Authentication Views
def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        user_type = request.POST.get('user_type')  # 'doctor' or 'patient'
        
        # Validation
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'main/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return render(request, 'main/register.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
            return render(request, 'main/register.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        # Create profile based on user type
        if user_type == 'doctor':
            DoctorProfile.objects.create(user=user)
            messages.success(request, 'Doctor account created successfully! Please complete your profile.')
        else:
            PatientProfile.objects.create(user=user)
            messages.success(request, 'Patient account created successfully!')
        
        login(request, user)
        return redirect('main:home_view')
    
    return render(request, 'main/register.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, f'Welcome back, {user.first_name or user.username}!')
            return redirect('main:home_view')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'main/login.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully')
    return redirect('main:home_view')

# Doctor Views
@login_required
def doctor_dashboard_view(request):
    try:
        doctor_profile = request.user.doctorprofile
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor profile not found')
        return redirect('main:home_view')
    
    # Get today's appointments
    today_appointments = Appointment.objects.filter(
        doctor=request.user,
        appointment_date=date.today()
    ).order_by('appointment_time')
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        doctor=request.user,
        appointment_date__gt=date.today(),
        status='scheduled'
    ).order_by('appointment_date', 'appointment_time')[:5]
    
    # Get recent consultations
    recent_consultations = Consultation.objects.filter(
        appointment__doctor=request.user
    ).order_by('-consultation_date')[:5]
    
    context = {
        'doctor_profile': doctor_profile,
        'today_appointments': today_appointments,
        'upcoming_appointments': upcoming_appointments,
        'recent_consultations': recent_consultations,
    }
    return render(request, 'main/doctor_dashboard.html', context)

@login_required
def doctor_profile_view(request):
    try:
        doctor_profile = request.user.doctorprofile
    except DoctorProfile.DoesNotExist:
        messages.error(request, 'Doctor profile not found')
        return redirect('main:home_view')
    
    if request.method == 'POST':
        # Update doctor profile
        doctor_profile.phone_number = request.POST.get('phone_number', '')
        doctor_profile.bio = request.POST.get('bio', '')
        doctor_profile.license_number = request.POST.get('license_number', '')
        doctor_profile.consultation_fee = request.POST.get('consultation_fee', 0)
        doctor_profile.years_experience = request.POST.get('years_experience', 0)
        
        specialty_id = request.POST.get('specialty')
        if specialty_id:
            doctor_profile.specialty_id = specialty_id
        
        doctor_profile.save()
        
        # Update user info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('main:doctor_profile_view')
    
    specialties = Specialty.objects.all()
    context = {
        'doctor_profile': doctor_profile,
        'specialties': specialties,
    }
    return render(request, 'main/doctor_profile.html', context)

# Patient Views
@login_required
def patient_dashboard_view(request):
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        messages.error(request, 'Patient profile not found')
        return redirect('main:home_view')
    
    # Get upcoming appointments
    upcoming_appointments = Appointment.objects.filter(
        patient=request.user,
        appointment_date__gte=date.today(),
        status='scheduled'
    ).order_by('appointment_date', 'appointment_time')
    
    # Get appointment history
    appointment_history = Appointment.objects.filter(
        patient=request.user
    ).order_by('-appointment_date', '-appointment_time')[:10]
    
    context = {
        'patient_profile': patient_profile,
        'upcoming_appointments': upcoming_appointments,
        'appointment_history': appointment_history,
    }
    return render(request, 'main/patient_dashboard.html', context)

@login_required
def patient_profile_view(request):
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        messages.error(request, 'Patient profile not found')
        return redirect('main:home_view')
    
    if request.method == 'POST':
        # Update patient profile
        patient_profile.phone_number = request.POST.get('phone_number', '')
        patient_profile.emergency_contact = request.POST.get('emergency_contact', '')
        
        date_of_birth = request.POST.get('date_of_birth')
        if date_of_birth:
            patient_profile.date_of_birth = date_of_birth
        
        patient_profile.save()
        
        # Update user info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('main:patient_profile_view')
    
    context = {
        'patient_profile': patient_profile,
    }
    return render(request, 'main/patient_profile.html', context)

# Doctor Listing and Booking Views
def doctors_list_view(request):
    doctors = DoctorProfile.objects.select_related('user', 'specialty').all()
    
    # Filter by specialty if provided
    specialty_filter = request.GET.get('specialty')
    if specialty_filter:
        doctors = doctors.filter(specialty_id=specialty_filter)
    
    # Filter by gender if provided
    gender_filter = request.GET.get('gender')
    if gender_filter:
        doctors = doctors.filter(gender=gender_filter)
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query and search_query.strip():
        # Remove common prefixes like "Dr." and "Doctor"
        clean_query = search_query.replace('Dr.', '').replace('Doctor', '').strip()
        
        # Split the search query into words for better matching
        search_words = clean_query.split()
        
        # Create Q objects for each word
        query_filters = Q()
        for word in search_words:
            if word:  # Skip empty words
                query_filters |= (
                    Q(user__first_name__icontains=word) |
                    Q(user__last_name__icontains=word)
                )
        
        # Also include specialty and bio search
        query_filters |= (
            Q(specialty__name__icontains=clean_query) |
            Q(bio__icontains=clean_query) |
            Q(specialty__name__icontains=search_query) |
            Q(bio__icontains=search_query)
        )
        
        doctors = doctors.filter(query_filters)
    
    specialties = Specialty.objects.all()
    gender_choices = DoctorProfile.GENDER_CHOICES
    
    context = {
        'doctors': doctors,
        'specialties': specialties,
        'gender_choices': gender_choices,
        'selected_specialty': specialty_filter,
        'selected_gender': gender_filter,
        'search_query': search_query,
    }
    return render(request, 'main/doctors_list.html', context)

@login_required
def book_appointment_view(request, doctor_id):
    # Check if user is a patient
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        messages.error(request, 'Only patients can book appointments')
        return redirect('main:home_view')
    
    doctor = get_object_or_404(User, id=doctor_id, doctorprofile__isnull=False)
    doctor_profile = doctor.doctorprofile
    
    if request.method == 'POST':
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        reason = request.POST.get('reason')
        
        # Check if appointment slot is available
        existing_appointment = Appointment.objects.filter(
            doctor=doctor,
            appointment_date=appointment_date,
            appointment_time=appointment_time
        ).first()
        
        if existing_appointment:
            messages.error(request, 'This time slot is already booked')
        else:
            # Create appointment
            appointment = Appointment.objects.create(
                patient=request.user,
                doctor=doctor,
                appointment_date=appointment_date,
                appointment_time=appointment_time,
                reason=reason
            )
            messages.success(request, 'Appointment booked successfully!')
            return redirect('main:patient_dashboard_view')
    
    context = {
        'doctor': doctor,
        'doctor_profile': doctor_profile,
    }
    return render(request, 'main/book_appointment.html', context)

@login_required
def manage_appointments_view(request):
    if hasattr(request.user, 'doctorprofile'):
        # Doctor view
        appointments = Appointment.objects.filter(
            doctor=request.user
        ).order_by('-appointment_date', '-appointment_time')
    elif hasattr(request.user, 'patientprofile'):
        # Patient view
        appointments = Appointment.objects.filter(
            patient=request.user
        ).order_by('-appointment_date', '-appointment_time')
    else:
        messages.error(request, 'Profile not found')
        return redirect('main:home_view')
    
    context = {
        'appointments': appointments,
    }
    return render(request, 'main/manage_appointments.html', context)

@login_required
@require_POST
def cancel_appointment_view(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    
    # Check if user can cancel this appointment
    if appointment.patient != request.user and appointment.doctor != request.user:
        messages.error(request, 'You are not authorized to cancel this appointment')
        return redirect('main:home_view')
    
    appointment.status = 'cancelled'
    appointment.save()
    
    messages.success(request, 'Appointment cancelled successfully')
    return redirect('main:manage_appointments_view')

# Static Pages
def about_view(request):
    return render(request, 'main/about.html')

def contact_view(request):
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        # Here you would typically save to database or send email
        messages.success(request, 'Thank you for your message! We will get back to you soon.')
        return redirect('main:contact_view')
    
    return render(request, 'main/contact.html')

# Medical Records Views
@login_required
def patient_medical_records_view(request):
    # Check if user is a patient
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        messages.error(request, 'Access denied. Patient profile required.')
        return redirect('main:home_view')
    
    records = PatientMedicalRecord.objects.filter(patient=request.user)
    return render(request, 'main/patient_medical_records.html', {'records': records})

@login_required
def upload_medical_record_view(request):
    # Check if user is a patient
    try:
        patient_profile = request.user.patientprofile
    except PatientProfile.DoesNotExist:
        messages.error(request, 'Access denied. Patient profile required.')
        return redirect('main:home_view')
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        record_type = request.POST.get('record_type')
        file = request.FILES.get('file')
        
        if title:
            record = PatientMedicalRecord.objects.create(
                patient=request.user,
                title=title,
                description=description,
                record_type=record_type,
                file=file
            )
            messages.success(request, 'Medical record uploaded successfully!')
            return redirect('main:patient_medical_records_view')
        else:
            messages.error(request, 'Please provide a title for the record.')
    
    return render(request, 'main/upload_medical_record.html')

@login_required
def delete_medical_record_view(request, record_id):
    record = get_object_or_404(PatientMedicalRecord, id=record_id, patient=request.user)
    
    if request.method == 'POST':
        # Delete the file if it exists
        if record.file:
            record.file.delete()
        record.delete()
        messages.success(request, 'Medical record deleted successfully!')
        return redirect('main:patient_medical_records_view')
    
    return render(request, 'main/delete_medical_record.html', {'record': record})

def public_medical_records_view(request):
    patient_id = request.GET.get('patient_id')
    records = []
    appointments = []
    patient_info = None
    
    if patient_id:
        try:
            # Try to find patient by user ID first
            patient = User.objects.get(id=patient_id)
            records = PatientMedicalRecord.objects.filter(patient=patient)
            patient_info = {
                'name': patient.get_full_name(),
                'email': patient.email,
                'id': patient.id
            }
        except User.DoesNotExist:
            # If not found by user ID, search in SimpleAppointment by patient_id field
            appointments = SimpleAppointment.objects.filter(patient_id=patient_id)
            if appointments.exists():
                first_appointment = appointments.first()
                patient_info = {
                    'name': first_appointment.patient_name,
                    'email': first_appointment.patient_email,
                    'id': patient_id
                }
            else:
                messages.error(request, 'Patient not found.')
    
    return render(request, 'main/public_medical_records.html', {
        'records': records,
        'appointments': appointments,
        'patient_info': patient_info,
        'patient_id': patient_id
    })

# Simple Appointment Booking Views (without authentication)
def book_appointment_view(request, doctor_id):
    doctor = get_object_or_404(DoctorProfile, id=doctor_id)
    
    if request.method == 'POST':
        patient_name = request.POST.get('patient_name')
        patient_email = request.POST.get('patient_email')
        patient_id = request.POST.get('patient_id')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        height = request.POST.get('height')
        weight = request.POST.get('weight')
        health_condition = request.POST.get('health_condition')
        health_document = request.FILES.get('health_document')
        appointment_date = request.POST.get('appointment_date')
        appointment_time = request.POST.get('appointment_time')
        
        if all([patient_name, patient_email, appointment_date, appointment_time]):
            try:
                appointment = SimpleAppointment.objects.create(
                    doctor=doctor,
                    patient_name=patient_name,
                    patient_email=patient_email,
                    patient_id=patient_id,
                    gender=gender if gender else None,
                    age=int(age) if age else None,
                    height=float(height) if height else None,
                    weight=float(weight) if weight else None,
                    health_condition=health_condition,
                    health_document=health_document,
                    appointment_date=appointment_date,
                    appointment_time=appointment_time
                )
                messages.success(request, f'Appointment booked successfully with Dr. {doctor.user.get_full_name()}!')
                return redirect('main:appointment_confirmation_view', appointment_id=appointment.id)
            except Exception as e:
                messages.error(request, 'This time slot is already booked. Please choose another time.')
        else:
            messages.error(request, 'Please fill in all required fields.')
    
    return render(request, 'main/book_appointment.html', {'doctor': doctor})

def appointment_confirmation_view(request, appointment_id):
    appointment = get_object_or_404(SimpleAppointment, id=appointment_id)
    return render(request, 'main/appointment_confirmation.html', {'appointment': appointment})

def my_appointments_view(request):
    email = request.GET.get('email')
    appointments = []
    
    if email:
        appointments = SimpleAppointment.objects.filter(patient_email=email).order_by('-appointment_date', '-appointment_time')
    
    return render(request, 'main/my_appointments.html', {
        'appointments': appointments,
        'email': email
    })
