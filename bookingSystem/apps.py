from django.apps import AppConfig
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime


class BookingsystemConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "bookingSystem"

    def ready(self):
        from bookingSystem.services import initStudents, execBookingSchedule
        from bookingSystem.scheduler import my_task

        # initStudents()
        scheduler = BackgroundScheduler()
        # UTC Time
        scheduler.add_job(initStudents, CronTrigger(hour=13, minute=0))
        scheduler.add_job(execBookingSchedule, CronTrigger(hour=13, minute=30))
        scheduler.start()

        # testing
        # scheduler.add_job(my_task, "date", run_date=datetime(2023, 5, 20, 12, 6, 0))
        # scheduler.add_job(my_task, "interval", seconds=1)
        # scheduler.add_job(
        #     execBookingSchedule, "date", run_date=datetime(2023, 5, 20, 15, 41, 0)
        # )
