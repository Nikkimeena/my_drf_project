from django.contrib import admin


from my_app.models import Student , CaptchaData


class StudentAdmin(admin.ModelAdmin):
    list_display=['first_name','last_name','email_id','phone_number','password','confirm_password']


admin.site.register(Student, StudentAdmin)
admin.site.register(CaptchaData)