from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Public pages
    path('', views.home_view, name='home_view'),
    path('about/', views.about_view, name='about_view'),
    path('contact/', views.contact_view, name='contact_view'),
    
    # Doctor listings (public)
    path('doctors/', views.doctors_list_view, name='doctors_list_view'),
    
    # My appointments (public - by email)
    path('my-appointments/', views.my_appointments_view, name='my_appointments_view'),
]