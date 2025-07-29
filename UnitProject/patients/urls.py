
    
from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    # Check appointment status (public)
    path('check-appointment/', views.check_appointment_status_view, name='check_appointment_status'),
    
    # Medical records
    path('my-medical-records/', views.patient_medical_records_view, name='patient_medical_records_view'),
    path('delete-medical-record/<int:record_id>/', views.delete_medical_record_view, name='delete_medical_record_view'),
    
    # Public medical records (no authentication required)
    path('medical-records/', views.public_medical_records_view, name='public_medical_records_view'),
] 