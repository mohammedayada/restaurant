import datetime
from rest_framework import generics
from rest_framework import serializers
from .models import (
    Table,
    Reservation,
)
from .serializers import (
    TableSerializer,
    ReservationSerializer,
)
from rest_framework.permissions import IsAuthenticated
from employee.permissions import IsAdminUser
from .filters import ReservationFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models.deletion import ProtectedError
from rest_framework import serializers


# List Tables view
class ListTablesView(generics.ListAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# Create table view
class CreateTableView(generics.CreateAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        # save logged user in created_by
        serializer.save(created_by=self.request.user)


# Delete table view
class DeleteTableView(generics.DestroyAPIView):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except ProtectedError:
            raise serializers.ValidationError({'table_protected': "table has reservations can not delete it"})
        return Response(status=204)


# List All Reservations view
class ListAllReservationsView(generics.ListAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReservationFilter


# List Today Reservations view
class ListTodayReservationsView(generics.ListAPIView):
    queryset = Reservation.objects.filter(date=datetime.datetime.today())
    serializer_class = ReservationSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['start_time', 'end_time']


# Delete Reservations view
class DeleteReservationView(generics.DestroyAPIView):
    queryset = Reservation.objects.filter(date=datetime.datetime.today())
    serializer_class = ReservationSerializer


# List all available time slots
class CheckAvailableTimeSlotsView(APIView):
    queryset = Reservation.objects.filter(date=datetime.datetime.today(), start_time__gte=datetime.datetime.now())

    def get(self, request, number_of_seats):
        """
        return list all available time slots in the system.
        parameters:
           number_of_seats
        """
        # check number of seats between 1 to 12
        if int(number_of_seats) > 12 or int(number_of_seats) < 1:
            return Response({'number_of_seats': 'should be between 1 to 12'}, status=400)

        # get all tables with required capacity
        tables_with_required_capacity = Table.objects.filter(number_of_seats__gte=number_of_seats).order_by(
            'number_of_seats').values_list('table_number', flat=True).distinct()
        tables_with_required_capacity = list(tables_with_required_capacity)

        # declare available time slots for all table

        available_time_slots = {table: [] for table in tables_with_required_capacity}
        # check available time in all tables
        for table in tables_with_required_capacity:

            # get all reservation for the table
            table_reservations = self.queryset.filter(table=table).order_by(
                'start_time').values('start_time', 'end_time')
            # check table available all the day
            if len(table_reservations) == 0:
                available_time_slots[table].append({'from': '12:00 PM', 'to': '11:59 PM'})
            else:
                # search time from now to end of working day
                search_time = datetime.datetime.now()

                # check in working day or not
                if search_time.hour < 12:
                    # if time not in working day start from begging working day 12 PM
                    search_time = datetime.time(hour=12, minute=0)

                # check available time slots in available table with required capacity
                for reservation in table_reservations:
                    # check search_time have reservation or not
                    # if search_time not have reservation add available slot to available_time_slots list
                    if search_time != reservation['start_time']:
                        # add available time to available_time_slots list
                        available_time_slots[table].append(
                            {
                                'from': search_time.strftime("%I:%M %p"),
                                'to': reservation['start_time'].strftime("%I:%M %p"),
                            }
                        )

                    # start time to search from end time of reservation
                    search_time = reservation['end_time']

                # check available time after last reservation in working day
                if search_time != datetime.time(hour=23, minute=59):
                    # add available time to available_time_slots list
                    available_time_slots[table].append(
                        {
                            'from': search_time.strftime("%I:%M %p"),
                            'to': datetime.time(hour=23, minute=59).strftime("%I:%M %p"),
                        }
                    )
        # return available time slots list
        return Response(available_time_slots)


# Create Reservation view
class CreateReservationView(generics.CreateAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def perform_create(self, serializer):
        # save logged user in created_by
        serializer.save(employee=self.request.user)
