from django.shortcuts import render,redirect
from .models import Student
from rest_framework.renderers import JSONRenderer
from .serializers import StudentSerializer
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate,logout



def register(request):
    # breakpoint()
    if request.method == 'POST':
        # breakpoint()
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
        student.save()
        # breakpoint()
        subject ="Welcome To My User Register From"
        email_message=f"Hello..{student.first_name} \n\nThank you for registering on our website. Please confirm your email address \n\nRegards,\nThe Django Team"
        form_email=settings.EMAIL_HOST_USER
        recipient_list=[student.email_id,]
        send_mail(subject, email_message, form_email, recipient_list)
        return redirect('home')
    
    return render(request, 'register.html')

"""
email and password get if check karna hai ki bhai email hai ki ni hai then check password if both asre is write then login and 
"""

def home(request):
    return render(request,'home.html')


def user_login(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')

        user = authenticate(request, email_id=email_id, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {email_id}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email_id or password. Please try again.')
    
    return render(request, 'index.html')