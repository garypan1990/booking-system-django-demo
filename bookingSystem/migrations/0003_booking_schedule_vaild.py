# Generated by Django 4.2.1 on 2023-05-18 07:56

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bookingSystem", "0002_rename_lessonid_booking_schedule_lesson_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="booking_schedule",
            name="vaild",
            field=models.BooleanField(default=True),
        ),
    ]
