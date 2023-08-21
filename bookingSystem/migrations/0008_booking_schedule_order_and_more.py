# Generated by Django 4.2.1 on 2023-05-24 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookingSystem', '0007_order_alter_booking_schedule_unique_together_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking_schedule',
            name='order',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='bookingSystem.order'),
        ),
        migrations.AlterUniqueTogether(
            name='booking_schedule',
            unique_together={('order', 'booking_start_time', 'booking_end_time')},
        ),
        migrations.DeleteModel(
            name='Order_Schedule',
        ),
    ]
