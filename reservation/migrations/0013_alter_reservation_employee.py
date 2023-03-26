# Generated by Django 4.0.6 on 2023-03-25 12:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0012_alter_reservation_client_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='employee',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
