from django.db import models
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.


class Member(models.Model):
    member_id = models.AutoField(primary_key=True)
    account = models.CharField(max_length=100, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birthday = models.DateField()
    hitutor_account = models.CharField(max_length=100)
    hitutor_password = models.CharField(max_length=100)
    email_address = models.CharField(max_length=100)
    created_time = models.DateTimeField(auto_now_add=True)
    note = models.CharField(max_length=1024)

    @property
    def age(self):
        today = date.today()
        age = today.year - self.birthday.year
        if today.month < self.birthday.month or (
            today.month == self.birthday.month and today.day < self.birthday.day
        ):
            age -= 1
        return age

    def __str__(self):
        return self.account


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    purchase_order_id = models.IntegerField(default=0)
    lesson_id = models.IntegerField(default=0)
    updated_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=True)
    note = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.order_id)


class Booking_Schedule(models.Model):
    booking_schedule_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, default=0)
    teacher_name = models.CharField(max_length=100)
    teacher_id = models.IntegerField(default=0)
    teaching_type = models.IntegerField(default=0)
    booking_start_time = models.DateTimeField(null=True)
    booking_end_time = models.DateTimeField(null=True)
    booking_status = models.BooleanField(null=True)
    updated_time = models.DateTimeField(auto_now=True)
    created_time = models.DateTimeField(auto_now_add=True)
    valid = models.BooleanField(default=True)
    note = models.TextField(blank=True)

    def __str__(self):
        return f"Booking Schedule ID: {self.booking_schedule_id}"

    class Meta:
        unique_together = (("order", "booking_start_time", "booking_end_time"),)
