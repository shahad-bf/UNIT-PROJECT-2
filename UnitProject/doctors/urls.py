from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    # Appointment management
    path('appointment/<int:appointment_id>/', views.appointment_detail_view, name='appointment_detail_view'),
    path('appointment/<int:appointment_id>/respond/', views.process_doctor_response, name='process_doctor_response'),
    
    # Public booking views (moved from main)
    path('book-appointment/<int:doctor_id>/', views.book_appointment_view, name='book_appointment_view'),
    path('appointment-confirmation/<int:appointment_id>/', views.appointment_confirmation_view, name='appointment_confirmation_view'),
] 