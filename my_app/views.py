from django.shortcuts import render,redirect
from .models import Student
from rest_framework.renderers import JSONRenderer
from .serializers import StudentSerializer
from django.http import HttpResponse
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import login,authenticate,logout
import time
import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException
import os
from dotenv import load_dotenv
from django.http import JsonResponse

load_dotenv()

from captcha.image import ImageCaptcha
import random
import string

def captcha_generate(captcha):
    image = ImageCaptcha(width=280, height=90)
    captcha_text = captcha
    data = image.generate(captcha_text)
    static_folder = 'static'
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
    image_path = os.path.join(static_folder, 'CAPTCHA.png')
    image.write(captcha_text, image_path)
    return image_path  # Return the path of the generated captcha image

def generate_captcha(length=6):
    captcha_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(captcha_characters) for _ in range(length))

def register(request):
    captcha = generate_captcha()
    captcha_data = captcha_generate(captcha) 
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
        configuration = sib_api_v3_sdk.Configuration()
        configuration.api_key['api-key'] = os.getenv("YOUR_API_V3_KEY")
        api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
        subject = "Demo Mail"
        sender = {"name": "Nikita Meena", "email": "nikita.jonwal@thoughtwin.com"}
        html_content = f"Hello {first_name} Welcome in Thoughtwin"
        to = [{"email": email, "name": first_name}]
        send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)

        try:
            api_response = api_instance.send_transac_email(send_smtp_email)
            student.save()
            response_data = {"message": "Email sent successfully!"}
        except ApiException as e:
            print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
        response = JsonResponse(response_data)
        response['X-Frame-Options'] = 'DENY'
        return redirect('home')
    return render(request, 'register.html',{'captcha_data':captcha_data})

"""
email and password get if check karna hai ki bhai email hai ki ni hai then check password if both asre is write then login and 
"""

def home(request):
    return render(request,'home.html')


def user_login(request):
    if request.method == 'POST':
        email_id = request.POST.get('email_id')
        password = request.POST.get('password')

        # user = authenticate(request, email_id=email_id, password=password)
        

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome, {email_id}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid email_id or password. Please try again.')
    
    return render(request, 'index.html')