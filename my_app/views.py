from django.shortcuts import render,redirect
from .models import Student
from .forms import StudentForm
from rest_framework.renderers import JSONRenderer
from .serializers import StudentSerializer
from django.http import HttpResponse
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email_id')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if not first_name or not last_name or not email or not phone_number or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('register')
        
    
        if Student.objects.filter(email_id=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email_id=email,
            phone_number=phone_number,
            password=password, 
            confirm_password=confirm_password
        )
        
        messages.success(request, "Registration successful. You can now login.")
        return redirect('home')
    
    return render(request, 'register.html')


def home(request):
    return render(request,'home.html')