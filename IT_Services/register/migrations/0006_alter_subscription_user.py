# Generated by Django 5.0.7 on 2024-08-10 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0005_login_is_active'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='user',
            field=models.CharField(max_length=100),
        ),
    ]
