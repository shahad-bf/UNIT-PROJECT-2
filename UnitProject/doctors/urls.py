from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    # Doctor dashboard
    path('dashboard/', views.doctor_dashboard_view, name='doctor_dashboard_view'),
    
    # Doctor profile management
    path('profile/', views.doctor_profile_view, name='doctor_profile_view'),
    
    # Appointment management
    path('appointment/<int:appointment_id>/', views.appointment_detail_view, name='appointment_detail_view'),
    path('appointment/<int:appointment_id>/respond/', views.process_doctor_response, name='process_doctor_response'),
    
    # Public booking views (moved from main)
    path('book-appointment/<int:doctor_id>/', views.book_appointment_view, name='book_appointment_view'),
    path('appointment-confirmation/<int:appointment_id>/', views.appointment_confirmation_view, name='appointment_confirmation_view'),
] 