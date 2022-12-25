from rest_framework import serializers
from .models import Reservation
from table.serializer import TableSerializer
from user.serializers import UserSerializer


class ReservationSerializer(serializers.ModelSerializer):
    table = TableSerializer()
    employee=UserSerializer()

    class Meta:
        model = Reservation
        fields = ['id', 'employee', 'table', 'start', 'end', 'required_seat']


class CreateReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['id', 'employee', 'table', 'start', 'end', 'required_seat']
