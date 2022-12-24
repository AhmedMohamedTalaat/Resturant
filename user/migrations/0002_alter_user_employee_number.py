# Generated by Django 4.1.4 on 2022-12-24 12:03

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='employee_number',
            field=models.CharField(max_length=4, unique=True, validators=[django.core.validators.MaxValueValidator(4), django.core.validators.MinValueValidator(4)]),
        ),
    ]
