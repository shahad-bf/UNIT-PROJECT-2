rom django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
from django.views.decorators.http import require_POST
from datetime import datetime, date

# Import models from other apps
from doctors.models import SimpleAppointment

# Simple view to show appointment status check
def check_appointment_status_view(request):
    appointments = None
    search_patient_id = None
    
    if request.method == 'POST':
        # Get search parameters
        patient_name = request.POST.get('patient_name', '').strip()
        search_patient_id = request.POST.get('patient_id', '').strip()
        
        if patient_name or search_patient_id:
            # Search for appointments
            appointments = SimpleAppointment.objects.all()
            
            if patient_name:
                appointments = appointments.filter(patient_name__icontains=patient_name)
            
            if search_patient_id:
                appointments = appointments.filter(patient_id__icontains=search_patient_id)
                
            appointments = appointments.order_by('-created_at')
    
    context = {
        'appointments': appointments,
        'search_patient_id': search_patient_id,
    }
    return render(request, 'patients/check_appointment_status.html', context)

# Note: Medical records functionality has been removed since it was not used in the frontend
def patient_medical_records_view(request):
    # This view is no longer functional since PatientMedicalRecord model was removed
    context = {
        'records': None,
        'message': 'Medical records functionality is currently not available.'
    }
    return render(request, 'patients/patient_medical_records.html', context)

def delete_medical_record_view(request, record_id):
    # This view is no longer functional since PatientMedicalRecord model was removed
    messages.error(request, "Medical records functionality is currently not available.")
    return redirect('patients:patient_medical_records_view')

def public_medical_records_view(request):
    # This view is no longer functional since PatientMedicalRecord model was removed
    context = {
        'records': None,
        'search_query': '',
        'record_types': [],
        'message': 'Medical records functionality is currently not available.'
    }
    return render(request, 'patients/public_medical_records.html', context)
