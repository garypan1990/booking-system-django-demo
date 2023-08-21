# Booking System

## Bugs
- [Fixed] when update the same day and same time but different teacher, it will find the first record and change it to valid. but the first record maybe the old teacher name
- [Fixed] when update schedule the date and the booking start time record already existed in DB but valid = false and scheduleId is different, it means there are two records, current is valid=true another is valid = false. The goal is modify current scheduleId to valid=False, and modify valid=False to True and update the schedule details 