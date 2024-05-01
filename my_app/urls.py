from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('home/',views.home,name='home'),
    path('login/',views.your_login_view,name='login'),
    path('Otp-verify/',views.otp_view,name='Otp-verify'),
]
