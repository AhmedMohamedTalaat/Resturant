from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
# Create your models here.


class User(AbstractUser):
    roles_choices = (('admin', 1), ('employee', 2))
    name = models.CharField(max_length=50, null=False, unique=True)
    employee_number = models.CharField(
        max_length=4, unique=True, validators=[MinLengthValidator(4)], null=False)
    role = models.CharField(
        max_length=20, choices=roles_choices, default='employee')
    USERNAME_FIELD = 'name'
