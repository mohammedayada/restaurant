from django.urls import path
from .views import (
    CreateTableView,
    DeleteTableView,
    ListAllReservationsView,
    ListTodayReservationsView,
    DeleteReservationView,
    CheckAvailableTimeSlotsView,
    ListTablesView,
    CreateReservationView,
)

urlpatterns = [
    path('table/list', ListTablesView.as_view(), name='list-tables'),
    path('table/create', CreateTableView.as_view(), name='create-table'),
    path('table/delete/<pk>', DeleteTableView.as_view(), name='delete-table'),
    path('table/reserve', CreateReservationView.as_view(), name='reserve-table'),
    path('reservation/all', ListAllReservationsView.as_view(), name='list-all-reservations'),
    path('reservation/today', ListTodayReservationsView.as_view(), name='list-today-reservations'),
    path('reservation/delete/<pk>', DeleteReservationView.as_view(), name='delete-reservation'),
    path('reservation/check-available-slots/<number_of_seats>', CheckAvailableTimeSlotsView.as_view(),
         name='check-available-slots-reservations'),
]
