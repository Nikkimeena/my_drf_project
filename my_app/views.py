from django.shortcuts import render,redirect
from .models import Student
from .forms import StudentForm
from rest_framework.renderers import JSONRenderer
from .serializers import StudentSerializer
from django.http import HttpResponse


def register(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  
    else:
        form = StudentForm()
    return render(request, 'index.html', {'form': form})



def home(request):
    return render(request,'home.html')