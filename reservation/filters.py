from .models import (
    Reservation,
)
from django_filters import rest_framework as filters


# Reservation Filter
class ReservationFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Reservation
        fields = ('date', 'table__table_number')
