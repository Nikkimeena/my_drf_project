from django.shortcuts import render
from .models import Student
from .forms import Studentform
from rest_framework.renderers import JSONRenderer
from .serializers import StudentSerializer
from django.http import HttpResponse

def register(request):
    regi=Student.objects.get(id=1)
    print(regi)
    serializers=StudentSerializer(regi)
    print(serializers)
    json_data=JSONRenderer().render(serializers.data)
    print(serializers.data)
    return HttpResponse(json_data,content_type='application/json')
    
