# Generated by Django 4.1.4 on 2022-12-24 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservation',
            name='is_reserved',
            field=models.BooleanField(default=0),
        ),
    ]