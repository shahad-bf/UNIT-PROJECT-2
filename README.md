# MediConsult - Medical Consultation System

## Project Description

**MediConsult** is a comprehensive Django-based medical consultation system that connects patients with healthcare providers. The system facilitates appointment booking and doctor-patient communication through a modern, user-friendly web interface.

The platform is designed to streamline the healthcare consultation process, allowing patients to easily find doctors, book appointments, and track their medical status while providing doctors with efficient tools to manage their practice and respond to patient consultations.

## Features List

### 🏥 Core Features
- **Doctor Directory**: Browse and search doctors by specialty, gender, and name
- **Appointment Booking**: Simple appointment booking system without requiring user registration
- **Appointment Tracking**: Patients can track appointment status using their Patient ID
- **Doctor Dashboard**: Comprehensive dashboard for doctors to manage appointments and respond to patients


### 💻 Technical Features
- **Responsive Design**: Mobile-friendly interface using Bootstrap and custom CSS
- **Database Integration**: MySQL database with Django ORM
- **Admin Panel**: Django admin interface for system administration
- **Search & Filter**: Advanced search and filtering capabilities

## User Stories

#On the medical consultation platform, the patient begins their journey by searching for the right doctor.
They can type keywords like “Psychiatrist” or “General Practitioner” into the search bar, or use filters to choose a specific specialty and preferred doctor gender (male or female).

Once the results appear, the patient selects a doctor and is taken to a detailed profile page.
Here, they can see the doctor's full name, specialty, consultation fee, years of experience, and gender.

If the patient is satisfied, they click the “Book Appointment” button.
They are directed to a form where they enter their personal information: full name, age, weight, height, gender, a description of their health condition, and their preferred appointment date.

After submitting the form, a confirmation page appears showing all appointment details, with the status marked as Pending (awaiting the doctor’s response).

Later, the doctor logs into their private dashboard using their email or ID.
They view the list of pending appointments, open one, and review the patient's information.

The doctor then writes a response, including a diagnosis and any treatment suggestions, and submits it.

Finally, the appointment status is updated to Completed, and the patient is notified that a response is now available.


Summarizing 

1. Search or Filter for a Doctor
Patient searches or filters by specialty and gender (e.g., Psychiatrist, General).
Both male and female doctors are available.

2. View Doctor Details
Patient sees doctor’s profile: name, specialty, fee, experience, and gender.

3. Book Appointment
Patient fills a form with personal info, health condition, and preferred date.

4. Confirm Appointment
A confirmation page shows doctor, patient, date, reason, and status: Pending.

5. Doctor Dashboard
Doctor logs in and sees all pending appointments.

6. Doctor Response
Doctor views patient info and submits diagnosis and recommendations.

7. Status Update
Status changes to Completed and the patient is notified.

## UML Diagram 

https://docs.google.com/document/d/13dpw8iMkcRr52bHXaxgNfqDgFaSmeIF9UOUSY9XHRuY/edit?usp=sharing



## Warefreame

https://www.canva.com/design/DAGub-BGReE/-2oaNVp_-5xsDsHBjQ9wbg/edit?utm_content=DAGub-BGReE&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton





## Technology Stack

- **Backend**: Django
- **Database**: MySQL 
- **Frontend**: HTML, CSS, Bootstrap 
- **UI Framework**: Material Symbols Icons, Custom CSS


## Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd UnitProject
   ```

2. **Install dependencies**:
   ```bash
   pip install django mysqlclient pillow
   ```

3. **Database setup**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create sample data**:
   ```bash
   python manage.py create_specialties
   python manage.py create_test_data
   ```

5. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

## Project Structure

```
UnitProject/
├── main/                    # Main application (home, doctors list)
├── doctors/                 # Doctor management and appointments
├── patients/                # Patient records and appointment tracking
├── media/                   # Uploaded files and documents
├── static/                  # CSS, JavaScript, and images
└── templates/              # HTML templates
```

## Usage

1. **Finding Doctors**: Browse the doctors directory and filter by specialty or gender
2. **Booking Appointments**: Select a doctor and fill out the appointment form
3. **Tracking Status**: Use your Patient ID to check appointment status and doctor responses
4. **Doctor Access**: Doctors can access their dashboard using their Doctor ID


## Currency

All consultation fees are displayed in Saudi Riyal using the abbreviation **ر.س.** 

