from rest_framework import serializers
from drf_app.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields=['name','number','email_id']

        """fiels lavel validation"""
    
    def validate_number(self, value):
        if len(str(value)) != 10:
            raise serializers.ValidationError("Number must be 10 digits")
        return value
    
    

# object lavel validation

# def validate(self, data):
#     nm = data.get('name')
#     if  nm[0].upper():
#         raise serializers.ValidationError("Please enter the name with the first character as uppercase.")
#     return nm


