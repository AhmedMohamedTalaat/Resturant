from django.db import models
from user.models import User
from table.models import Table
# Create your models here.


class Reservation(models.Model):
    employee = models.ForeignKey(User, on_delete=models.CASCADE)
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()
    required_seat = models.IntegerField(default=1, null=False)
    is_reserved=models.BooleanField(default=1)

    class Meta:
        db_table = 'reservation'



