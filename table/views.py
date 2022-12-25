from rest_framework.generics import ListCreateAPIView
from .models import Table
from .serializer import TableSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.exceptions import AuthenticationFailed
from django.core.exceptions import PermissionDenied
from rest_framework.response import Response
from reservation.models import Reservation
from datetime import datetime, date
from rest_framework import status
from reservation.help import get_role
# Create your views here.


class TableView(ListCreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer

    def get(self, requet):
        queryset = self.get_queryset()
        serializer = TableSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TableSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request):
        if get_role(request) == 'admin':
            table = request.date['table']
            if table:
                reserved = Reservation.objects.filter(
                    end__lte=datetime.now(), table__number=table)
                if reserved.count():
                    Response(
                        {"message": "Delete this table not avaiable beacuse it reserved today!"})
                else:
                    Response({"message": "Selected table deleted!"},
                             status=status.HTTP_204_NO_CONTENT)
        else:
            Response({"message": "Only admin authorized to perform that operation!"},
                     status=status.HTTP_401_UNAUTHORIZED)
