from django.urls import path, include
from .views import AllReservationView,AvaliableReservationSlotView

urlpatterns = [
    path('', AllReservationView.as_view()),
    path('available-slots/',AvaliableReservationSlotView.as_view())
]
