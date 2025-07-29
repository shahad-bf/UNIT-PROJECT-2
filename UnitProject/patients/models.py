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
        ('other', 'Other'),
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

# Extended User model to create Patient Profile  
class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Direct link to Django user
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True)
    # Additional fields can be added: address, medical history (with strict privacy)

    def __str__(self):
        return f"Patient {self.user.first_name} {self.user.last_name}"

# Appointments Model
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

    class Meta:
        # Prevent duplicate appointments for the same doctor at the same time
        unique_together = ('doctor', 'appointment_date', 'appointment_time')
        ordering = ['appointment_date', 'appointment_time']

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

# Patient Medical Records Model
class PatientMedicalRecord(models.Model):
    RECORD_TYPE_CHOICES = [
        ('lab_result', 'Lab Result'),
        ('xray', 'X-Ray'),
        ('prescription', 'Prescription'),
        ('report', 'Medical Report'),
        ('image', 'Medical Image'),
        ('document', 'Medical Document'),
    ]
    
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medical_records')
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    record_type = models.CharField(max_length=20, choices=RECORD_TYPE_CHOICES, default='document')
    file = models.FileField(upload_to='medical_records/%Y/%m/%d/', blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date_created']
    
    def __str__(self):
        return f"{self.title} - {self.patient.username}"

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
        ('other', 'Other'),
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
    health_document = models.FileField(upload_to='appointment_documents/%Y/%m/%d/', blank=True, null=True, help_text="Upload PDF or medical document")
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['doctor', 'appointment_date', 'appointment_time']
    
    def __str__(self):
        return f"{self.patient_name} - Dr. {self.doctor.user.get_full_name()} on {self.appointment_date}"

# Doctor Availability Model
class DoctorAvailability(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability_slots')
    day_of_week = models.CharField(max_length=10, choices=[
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'), 
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    ])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('doctor', 'day_of_week', 'start_time')

    def __str__(self):
        return f"Dr. {self.doctor.username} - {self.day_of_week} {self.start_time}-{self.end_time}"