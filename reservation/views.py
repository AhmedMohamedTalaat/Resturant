from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from .serializer import ReservationSerializer, CreateReservationSerializer
from .models import Reservation
from table.models import Table
from rest_framework.response import Response
from datetime import datetime, date
from .help import time_in_range, convert_12_format, get_role
from django.db.models import Q
from rest_framework import status

# Create your views here.


class AllReservationView(ListCreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    paginate_by = 10

    def get(self, request, **kwargs):
        # admin can retrive all reservations
        if get_role(request) == 'admin':
            queryset = self.get_queryset()
            if self.request.GET.get('table'):
                queryset = queryset.filter(table=self.request.GET.get('table'))
            if self.request.GET.get('start') and self.request.GET.get('end'):
                queryset = queryset.filter(start__range=(
                    self.request.GET.get('start'), self.request.GET.get('end')))
                print(queryset.query)
            serializer = ReservationSerializer(queryset, many=True)
            return Response(serializer.data)
        else:
            # employee can get reservations for today.
            queryset = Reservation.objects.filter(start=datetime.date())
            serializer = ReservationSerializer(queryset, many=True)
            return Response(serializer.data)

    # create new reservation
    def post(self, request):
        serializer = CreateReservationSerializer(data=self.request.data)
        # check if the slot is revesed by another employee.
        is_reseved = Reservation.objects.filter(
            table__pk=request.data['table'], start__contains=date.today())
        if is_reseved.count():
            for t in is_reseved:
                start = datetime.strptime(request.data['start'], '%Y-%m-%d %H:%M:%S').time()
                end = datetime.strptime(request.data['end'], '%Y-%m-%d %H:%M:%S').time()
                if t.start.time() == start or t.end.time() == end:
                    return Response({"message": f"this slot is not available."})
        # save the reservation for the table
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # delete reservation for today
    def delete(self, request):
        reservation = Reservation.objects.filter(
            pk=request.data['id'], start__contains=date.today())
        reservation.delete()
        return Response({'message': 'Reservation deleted!'}, status=status.HTTP_204_NO_CONTENT)


class AvaliableReservationSlotView(ListCreateAPIView):
    def get(self, request):
        from datetime import time
        reserved_list = []
        start = time(1, 0)
        end = time(23, 59)
        current = datetime.now().time()
        tables = None
        seats = self.request.GET.get('seats')
        if int(seats) > 12 or int(seats) == 0:
            return Response({"message": "There is no available table!"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        if seats:
            tables = Table.objects.filter(seat__lte=seats)
        reservations = Reservation.objects.filter(start__contains=date.today(), table__seat__lte=seats).order_by('start')
        for r in reservations:
            reserved_list.append((convert_12_format(r.start.hour, r.start.minute), convert_12_format(r.end.hour, r.end.minute)))
        if reservations.count() == 0:
            return Response({"available": f"{convert_12_format(current.hour,current.minute)} - {convert_12_format(end.hour,end.minute)}"})
        if reservations:
            return Response({"those slots are reservered ": reserved_list})
        else:
            return Response({"available": f"{convert_12_format(current.hour,current.minute)} - {convert_12_format(end.hour,end.minute)}"})
