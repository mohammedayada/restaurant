# Generated by Django 4.1.7 on 2023-03-26 00:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0013_alter_reservation_employee'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='reservation.table'),
        ),
    ]
