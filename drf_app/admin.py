from django.contrib import admin
from drf_app.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=['name','number','email_id']
admin.site.register(User,UserAdmin)