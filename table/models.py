from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.


class Table(models.Model):
    number = models.IntegerField(default=0, null=False, unique=True)
    seat = models.IntegerField(null=False, default=1, validators=[
                               MinValueValidator(1), MaxValueValidator(12)])

    class Meta:
        db_table = 'table'
    
