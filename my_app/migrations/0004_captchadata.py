# Generated by Django 4.2.11 on 2024-04-30 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('my_app', '0003_studentlogin'),
    ]

    operations = [
        migrations.CreateModel(
            name='CaptchaData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('captcha_data', models.CharField(max_length=6)),
            ],
        ),
    ]