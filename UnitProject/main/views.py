from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

def home_view(request:HttpResponse):

    return render(request, "main/home.html")

# Create your views here.
