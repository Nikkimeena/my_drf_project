from django.contrib import admin
from drf_app.models import User,Book

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display=['name','number','email_id']
admin.site.register(User,UserAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display=['book_name','author_name','published_date']
admin.site.register(Book,BookAdmin)