# Generated by Django 4.2.1 on 2023-05-24 05:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bookingSystem', '0006_alter_booking_schedule_unique_together'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(primary_key=True, serialize=False)),
                ('purchase_order_id', models.IntegerField(default=0)),
                ('lesson_id', models.IntegerField(default=0)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(max_length=1024)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookingSystem.member')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='booking_schedule',
            unique_together=set(),
        ),
        migrations.CreateModel(
            name='Order_Schedule',
            fields=[
                ('order_schedule_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('note', models.CharField(max_length=1024)),
                ('booking_schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookingSystem.booking_schedule')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookingSystem.order')),
            ],
        ),
        migrations.RemoveField(
            model_name='booking_schedule',
            name='lesson_id',
        ),
        migrations.RemoveField(
            model_name='booking_schedule',
            name='member_id',
        ),
        migrations.RemoveField(
            model_name='booking_schedule',
            name='purchase_order_id',
        ),
    ]
