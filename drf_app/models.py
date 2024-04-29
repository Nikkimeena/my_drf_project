from django.db import models

# Create your models here.
class User(models.Model):
    name=models.CharField(max_length=100)
    number=models.IntegerField()
    email_id=models.EmailField()


    def __str__(self):
        return self.name
        
   
class Book(models.Model):
    book_name=models.CharField(max_length=90)
    author_name=models.CharField(max_length=90)
    published_date=models.DateTimeField(auto_now=True)
