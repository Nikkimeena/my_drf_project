from django.shortcuts import render,redirect
from .models import Student ,CaptchaData,StudentLogin
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

def otp_generate():
    otp = random.randint(100000, 999999)
    return otp


def captcha_generate(captcha):
    image = ImageCaptcha(width=280, height=90)
    captcha_text = captcha
    data = image.generate(captcha_text)
    static_folder = 'static'
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)
    image_path = os.path.join(static_folder, 'CAPTCHA.png')
    image.write(captcha_text, image_path)
    return image_path 

def generate_captcha(length=6):
    captcha_characters = string.ascii_letters + string.digits
    return ''.join(random.choice(captcha_characters) for _ in range(length))

def register(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email_id')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_captcha=request.POST.get('user_captcha')
        
        if not first_name or not last_name or not email or not phone_number or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect('register')
        
    
        if Student.objects.filter(email_id=email).exists():
            messages.error(request, "Email is already registered.")
            return redirect('register')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        
        data = CaptchaData.objects.last()
        if data.captcha_data != user_captcha:
            messages.error(request,"Captcha do not match.")
            return redirect('register')
        
        student = Student.objects.create(
            first_name=first_name,
            last_name=last_name,
            email_id=email,
            phone_number=phone_number,
            password=password, 
            confirm_password=confirm_password,

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
        return redirect('login')
    captcha = generate_captcha()
    captcha_data = captcha_generate(captcha)
    print(captcha,"-----")
    data_value = CaptchaData.objects.create(captcha_data=captcha)
    data_value.save()
    return render(request, 'register.html',{'captcha_data':captcha_data})

def home(request):
    return render(request,'home_page.html')

def your_login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email_id')
        password = request.POST.get('pass')
        try:
            user = Student.objects.get(email_id=email)
            otp = otp_generate()
            print(otp)
            if user.password == password:
                configuration = sib_api_v3_sdk.Configuration()
                configuration.api_key['api-key'] = os.getenv("YOUR_API_V3_KEY")
                api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
                subject = "Demo Mail"
                sender = {"name": "Nikita Meena", "email": "nikita.jonwal@thoughtwin.com"}
                html_content = f"""<div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
                        <div style="margin:50px auto;width:70%;padding:20px 0">
                        <div style="border-bottom:1px solid #eee">
                            <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">Your Brand</a>
                        </div>
                        <p style="font-size:1.1em">Hi,</p>
                        <p>Thank you for choosing thise side. Use the following OTP to complete your Sign Up procedures. OTP is valid for 5 minutes</p>
                        <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
                        <p style="font-size:0.9em;">Regards,<br />Nikita JOnwal</p>
                        <hr style="border:none;border-top:1px solid #eee" />
                        <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
                            <p>Your Brand Inc</p>
                            <p>1600 Amphitheatre Parkway</p>
                            <p>California</p>
                        </div>
                        </div>
                </div>"""
                to = [{"email": email}]
                send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, html_content=html_content, sender=sender, subject=subject)
                try:
                    api_response = api_instance.send_transac_email(send_smtp_email)
                    users = StudentLogin.objects.create(
                                    email_id=email,
                                    user_otp=otp,
                    )
                    users.save()
                    response_data = {"message": "Email sent successfully!"}
                    return redirect('Otp-verify')
                except ApiException as e:
                    print("Exception when calling SMTPApi->send_transac_email: %s\n" % e)
                    response = JsonResponse(response_data)
                    response['X-Frame-Options'] = 'DENY'

        except Student.DoesNotExist:
            return render(request, 'index.html', {'error_message': 'User does not exist'})
    else:
        return render(request, 'index.html')

def otp_view(request):
    if request.method == 'POST':
        number1 = request.POST.get('number1')
        number2 = request.POST.get('number2')
        number3 = request.POST.get('number3')
        number4 = request.POST.get('number4')
        number5 = request.POST.get('number5')
        number6 = request.POST.get('number6')
        entered_otp = "".join([number1, number2, number3, number4, number5, number6])
        try:
            stu_log = StudentLogin.objects.last()
            model_enter_otp = stu_log.user_otp
            if entered_otp == model_enter_otp:
                return redirect('home')
            else:
                # return redirect('Otp-verify')
                pass
        except StudentLogin.DoesNotExist:
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request,'otpverify.html')
