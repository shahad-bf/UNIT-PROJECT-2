from django.db import models
from django.contrib.auth.models import User  # Using Django's default User model

# Medical Specialties Model
class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Specialties"

# Extended User model to create Doctor Profile
class DoctorProfile(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
       
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Direct link to Django user
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)
    license_number = models.CharField(max_length=50, unique=True, blank=True, null=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    years_experience = models.PositiveIntegerField(default=0)
    # Additional fields can be added: profile picture, working hours, clinic address

    def __str__(self):
        return f"Dr. {self.user.first_name} {self.user.last_name} ({self.specialty})"

# Simple Appointment Model (without authentication)
class SimpleAppointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
      
    ]
    
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='simple_appointments')
    patient_name = models.CharField(max_length=100)
    patient_email = models.EmailField()
    patient_phone = models.CharField(max_length=20)
    patient_id = models.CharField(max_length=50, blank=True, null=True, help_text="Patient ID for linking to medical records")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Height in cm")
    weight = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, help_text="Weight in kg")
    health_condition = models.TextField(blank=True, help_text="Description of current health condition")
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    doctor_response = models.TextField(blank=True, null=True, help_text="Doctor's response and diagnosis")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
    
    def __str__(self):
        return f"{self.patient_name} - Dr. {self.doctor.user.get_full_name()} on {self.appointment_date}"

# Appointments Model (for authenticated users)
class Appointment(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='patient_appointments')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='doctor_appointments')
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status_choices = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    status = models.CharField(max_length=15, choices=status_choices, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"Appointment for {self.patient.username} with Dr. {self.doctor.username} on {self.appointment_date} at {self.appointment_time}"

# Consultation Model (Doctor's notes after appointment)
class Consultation(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, unique=True)
    diagnosis = models.TextField()
    treatment_plan = models.TextField()
    prescription = models.TextField(blank=True, null=True)  # Medical prescription
    follow_up_required = models.BooleanField(default=False)
    follow_up_date = models.DateField(blank=True, null=True)
    consultation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Consultation for {self.appointment.patient.username} on {self.consultation_date.date()}"

