from datetime import datetime, time
from rest_framework import serializers
from .models import (
    Table,
    Reservation,
)


# Table serializer
class TableSerializer(serializers.ModelSerializer):
    created_by = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Table
        fields = '__all__'


# Reservation serializer
class ReservationSerializer(serializers.ModelSerializer):
    def validate(self, data):
        # check date before now
        if data['date'] < datetime.now().date():
            raise serializers.ValidationError("Date must be in future.")

        # check start time before end time
        if data['start_time'] > data['end_time']:
            raise serializers.ValidationError("End time must be after start time.")

        # check start time in working day hours
        if data['start_time'] < time(12, 0):
            raise serializers.ValidationError("Start time must be in working day hours.")

        # # check start time before now
        # if data['start_time'] > datetime.now().time() and data['date'] == datetime.now().date():
        #     raise serializers.ValidationError("start time must be in future.")

        # get table reservations for this table, day
        table_reservations = Reservation.objects.filter(table=data['table'], date=data['date']).order_by(
            'start_time').values('start_time', 'end_time')
        # check overlap
        for reservation in table_reservations:
            if (reservation['start_time'] <= data['end_time']) and (data['start_time'] <= reservation['end_time']):
                raise serializers.ValidationError("Table have reservation at this time")
        return data

    employee = serializers.StringRelatedField(default=serializers.CurrentUserDefault(), read_only=True)

    class Meta:
        model = Reservation
        fields = '__all__'
