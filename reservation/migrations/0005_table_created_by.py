# Generated by Django 4.0.6 on 2023-03-24 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0004_remove_table_id_alter_table_table_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='table',
            name='created_by',
            field=models.CharField(default=1000, max_length=40),
            preserve_default=False,
        ),
    ]
