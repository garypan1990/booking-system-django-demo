# Generated by Django 4.2.1 on 2023-05-18 07:37

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("bookingSystem", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="booking_schedule",
            old_name="lessonId",
            new_name="lesson_id",
        ),
        migrations.RenameField(
            model_name="booking_schedule",
            old_name="purchaseOrderId",
            new_name="purchase_order_id",
        ),
        migrations.RenameField(
            model_name="booking_schedule",
            old_name="teachingType",
            new_name="teaching_type",
        ),
    ]
