# Generated by Django 4.0.6 on 2023-03-24 19:07

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reservation', '0005_table_created_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='created_by', to=settings.AUTH_USER_MODEL),
        ),
    ]
