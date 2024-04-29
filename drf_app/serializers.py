from rest_framework import serializers
from drf_app.models import User,Book


""" 1.validation """
def start_with_r(value):
    if value[0].lower() !='r':
        raise serializers.ValidationError("name should be start with r")



class UserSerializer(serializers.ModelSerializer):
    name=serializers.CharField(max_length=100) #one field ke liye
    class Meta:
        model = User
        fields=['name','number','email_id']
        # read_only_fields=['name','number'] ## if you need multiple fields

        """2. fiels level validation"""
    
    # def validate_number(self, value):
    #     if len(str(value)) != 10:
    #         raise serializers.ValidationError("Number must be 10 digits")
    #     return value
    
    

# 3. object level validation

# def validate(self, data):
#     nm = data.get('name')
#     if  nm[0].upper():
#         raise serializers.ValidationError("Please enter the name with the first character as uppercase.")
#     return nm



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields=['book_name','author_name','published_date']