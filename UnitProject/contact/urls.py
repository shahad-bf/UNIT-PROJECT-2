from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Public pages
    path('', views.home_view, name='home_view'),
    path('about/', views.about_view, name='about_view'),
    path('contact/', views.contact_view, name='contact_view'),
    
    # Doctor listings
    path('doctors/', views.doctors_list_view, name='doctors_list_view'),
    
    # Appointment booking (no authentication required)
    path('book-appointment/<int:doctor_id>/', views.book_appointment_view, name='book_appointment_view'),
    path('appointment-confirmation/<int:appointment_id>/', views.appointment_confirmation_view, name='appointment_confirmation_view'),
    path('my-appointments/', views.my_appointments_view, name='my_appointments_view'),
    
    # Medical records (public access)
    path('medical-records/', views.public_medical_records_view, name='public_medical_records_view'),
    
    # Protected medical records (with authentication)
    path('my-medical-records/', views.patient_medical_records_view, name='patient_medical_records_view'),
    path('upload-medical-record/', views.upload_medical_record_view, name='upload_medical_record_view'),
    path('delete-medical-record/<int:record_id>/', views.delete_medical_record_view, name='delete_medical_record_view'),
]