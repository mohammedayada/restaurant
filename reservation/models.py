from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
import datetime
from django.core.exceptions import ValidationError


# Create your models here.
class Table(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='created_by',
                                   blank=True, null=True)
    table_number = models.PositiveSmallIntegerField(primary_key=True)
    number_of_seats = models.PositiveIntegerField(validators=[MaxValueValidator(12), MinValueValidator(1)])

    def __str__(self):
        return "{}".format(self.table_number)


class Reservation(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True,null=True, on_delete=models.SET_NULL)
    table = models.ForeignKey(Table, on_delete=models.PROTECT)
    client_name = models.CharField(max_length=100, blank=True, null=True)
    client_phone_number = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    number_of_people = models.PositiveIntegerField(blank=True, null=True,
                                                   validators=[MaxValueValidator(12), MinValueValidator(1)])

    class Meta:
        unique_together = ('start_time', 'date', 'table')
        ordering = ('-pk',)
