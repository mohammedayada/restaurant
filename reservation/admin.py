from django.contrib import admin
from .models import (
    Table,
    Reservation,
)


# Table
class TableAdmin(admin.ModelAdmin):
    list_display = ('table_number', 'number_of_seats')


admin.site.register(Table, TableAdmin)


# Reservation
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('table', 'date', 'start_time', 'end_time',)

    def has_add_permission(self, request, obj=None):
        return False


admin.site.register(Reservation, ReservationAdmin)
