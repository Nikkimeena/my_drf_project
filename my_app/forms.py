from django import forms
from my_app.models import Student


class Studentform(forms.ModelForm):
    class Meta:
        model=Student
        fields="__all__"