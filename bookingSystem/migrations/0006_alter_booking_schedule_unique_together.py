# Generated by Django 4.2.1 on 2023-05-18 15:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookingSystem', '0005_alter_booking_schedule_unique_together'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='booking_schedule',
            unique_together={('member_id', 'booking_start_time', 'booking_end_time')},
        ),
    ]
