import json
from bookingSystem.utilities import addBookingScheduleForm, registerForm, addOrderForm
from .models import Member, Booking_Schedule, Order
from datetime import datetime, timedelta, timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction, IntegrityError
from django.db.models import F
from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, "bookingSystem/index.html")


@require_http_methods(["GET"])
@csrf_exempt
def memberList(request):
    members = Member.objects.all()
    member_data = []
    for member in members:
        orders = list(
            Order.objects.filter(member=member, valid=True).values(
                orderId=F("order_id"),
                purchaseOrderId=F("purchase_order_id"),
                lessonId=F("lesson_id"),
            )
        )
        member_data.append(
            {
                "memberId": member.member_id,
                "firstName": member.first_name,
                "lastName": member.last_name,
                "account": member.account,
                "hiTutorAccount": member.hitutor_account,
                "createdTime": member.created_time,
                "orders": orders,
            }
        )
    return JsonResponse(member_data, safe=False)


@require_http_methods(["POST"])
@csrf_exempt
def register(request):
    try:
        data = json.loads(request.body)
        form = registerForm(data)
        account = data.get("account")
        first_name = data.get("firstName")
        last_name = data.get("lastName")
        birthday = data.get("birthday")
        hitutor_account = data.get("hitutorAccount")
        hitutor_password = data.get("hitutorPassword")
        email_address = data.get("emailAddress")

        if not form.is_valid():
            for field, errors in form.errors.items():
                return JsonResponse({"message": f"{field} is invalid"}, status=400)

        member = Member(
            account=account,
            first_name=first_name,
            last_name=last_name,
            birthday=birthday,
            hitutor_account=hitutor_account,
            hitutor_password=hitutor_password,
            email_address=email_address,
        )
        member.save()

        return HttpResponse()
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"message": "Registration failed"}, status=400)


@require_http_methods(["POST"])
@csrf_exempt
def addOrder(request):
    try:
        data = json.loads(request.body)
        form = addOrderForm(data)
        account = data.get("account")
        purchaseOrderId = data.get("purchaseOrderId")
        lessonId = data.get("lessonId")

        if not form.is_valid():
            for field, errors in form.errors.items():
                return JsonResponse({"message": f"{field} is invalid"}, status=400)

        try:
            member = Member.objects.get(account=account)
        except Member.DoesNotExist:
            return JsonResponse({"message": "account is not exist"}, status=400)

        try:
            result = Order.objects.filter(
                member=member, purchase_order_id=purchaseOrderId
            ).values()
            result = list(result)
            if len(result) != 0:
                raise Exception("purchase order id existed.")
        except Exception as e:
            return JsonResponse({"message": f"{e}"}, status=400)
        order = Order(
            member=member,
            purchase_order_id=purchaseOrderId,
            lesson_id=lessonId,
        )
        order.save()

        return JsonResponse({"message": "add order successfully."})
    except json.JSONDecodeError:
        return JsonResponse({"message": "Invalid JSON data"}, status=400)
    except Exception as e:
        print(e)
        return JsonResponse({"message": f"add order failed, reason:{e}"}, status=400)


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteOrder(request, account, orderId):
    print("deleteOrder")
    try:
        try:
            member = Member.objects.get(account=account)
            order = Order.objects.select_related("member").get(
                member=member, order_id=orderId
            )
            result = Order.objects.filter(
                order_id=orderId,
                valid=True,
            ).values()
            print(result)
            result = list(result)
            if len(result) == 0:
                raise Exception
        except Exception as e:
            return JsonResponse({"message": "orderId not found"}, status=400)
        try:
            with transaction.atomic():
                order = Order.objects.get(order_id=orderId)
                order.valid = False
                order.save()
                return JsonResponse({"message": "delete order sucessfully"})
        except Booking_Schedule.DoesNotExist:
            return JsonResponse({"message": "order not found"}, status=400)
    except Exception as e:
        return JsonResponse({"message": f"{e}"}, status=400)


@require_http_methods(["GET"])
def getBookSchedule(request):
    account = request.GET.get("account")
    purchaseOrderId = request.GET.get("purchaseOrderId")
    member = Member.objects.get(account=account)

    order = Order.objects.select_related("member").get(
        member=member, purchase_order_id=purchaseOrderId
    )

    results = (
        Booking_Schedule.objects.select_related("order")
        .filter(order=order, valid=True)
        .values(
            bookingScheduleId=F("booking_schedule_id"),
            # purchaseOrderId=F("purchase_order_id"),
            # lessonId=F("lesson_id"),
            purchaseOrderId=F("order__purchase_order_id"),
            lessonId=F("order__lesson_id"),
            teacherId=F("teacher_id"),
            teacherName=F("teacher_name"),
            teachingType=F("teaching_type"),
            bookingStartTime=F("booking_start_time"),
            bookingEndTime=F("booking_end_time"),
            bookingStatus=F("booking_status"),
        )
    )

    data = list(results)

    return JsonResponse(data, safe=False)


@require_http_methods(["POST"])
@csrf_exempt
def addBookSchedule(request):
    try:
        data = json.loads(request.body)
        form = addBookingScheduleForm(data)
        account = data.get("account")
        orderId = data.get("orderId")
        teacherName = data.get("teacherName")
        teacherId = data.get("teacherId")
        # purchaseOrderId = data.get("purchaseOrderId")
        # lessonId = data.get("lessonId")
        teachingType = data.get("teachingType")
        schedules = data.get("schedules")

        if not form.is_valid():
            for field, errors in form.errors.items():
                return JsonResponse({"message": f"{field} is invalid"}, status=400)

        try:
            member = Member.objects.get(account=account)

        except Member.DoesNotExist:
            return JsonResponse({"message": "account is not exist"}, status=400)

        bookingStartTime = datetime.strptime(
            data.get("bookingStartTime"), "%Y-%m-%dT%H:%M:%SZ"
        )
        bookingEndTime = datetime.strptime(
            data.get("bookingEndTime"), "%Y-%m-%dT%H:%M:%SZ"
        )
        if bookingEndTime <= bookingStartTime:
            return JsonResponse(
                {
                    "message": "The booking start time must be before the booking end time"
                },
                status=400,
            )
        try:
            order = Order.objects.get(member=member.member_id, order_id=orderId)

        except Order.DoesNotExist:
            return JsonResponse({"message": "order is not exist"}, status=400)
        # return HttpResponse(True)
        try:
            with transaction.atomic():
                for schedule in schedules:
                    records = Booking_Schedule.objects.filter(
                        order=order,
                        booking_start_time=schedule["bookingStartTime"],
                        booking_end_time=schedule["bookingEndTime"],
                    ).first()

                    if records and records.valid == False:
                        records.teacher_id = teacherId
                        records.teacher_name = teacherName
                        records.teaching_type = teachingType
                        records.valid = True
                        records.save()
                    else:
                        bookingSchedule = Booking_Schedule(
                            order=order,
                            teacher_name=teacherName,
                            teacher_id=teacherId,
                            teaching_type=teachingType,
                            booking_start_time=schedule["bookingStartTime"],
                            booking_end_time=schedule["bookingEndTime"],
                        )
                        bookingSchedule.save()

                return JsonResponse({"message": "booking successful."})
        except IntegrityError as e:
            return JsonResponse(
                {"message": f"You have already booked the class in {schedules}"},
                status=400,
            )
        except Exception as e:
            print(f"add booking schedule failed. reason: {e}")
            return JsonResponse({"error": str(e)}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"message": "invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"message": "Registration failed"}, status=400)


@require_http_methods(["PUT"])
@csrf_exempt
def updateBookSchedule(request):
    try:
        data = json.loads(request.body)
        bookingScheduleId = data.get("bookingScheduleId")
        orderId = data.get("orderId")

        bookingStartTime = data.get("bookingStartTime")
        bookingEndTime = data.get("bookingEndTime")
        teacherId = data.get("teacherId")
        teacherName = data.get("teacherName")
        teachingType = data.get("teachingType")

        bookingStartTime = datetime.strptime(
            data.get("bookingStartTime"), "%Y-%m-%dT%H:%M:%SZ"
        )
        bookingEndTime = datetime.strptime(
            data.get("bookingEndTime"), "%Y-%m-%dT%H:%M:%SZ"
        )
        if bookingEndTime <= bookingStartTime:
            return JsonResponse(
                {
                    "message": "The booking start time must be before the booking end time"
                },
                status=400,
            )
        records = None
        try:
            records = Booking_Schedule.objects.get(
                valid=False,
                booking_start_time=bookingStartTime,
                booking_end_time=bookingEndTime,
                order_id=orderId,
            )
        except Booking_Schedule.DoesNotExist:
            pass

        if records:
            try:
                bookschedule = Booking_Schedule.objects.get(
                    booking_schedule_id=bookingScheduleId, valid=True, order_id=orderId
                )
            except Booking_Schedule.DoesNotExist:
                return JsonResponse(
                    {"message": "booking schedule is not exist"}, status=400
                )
            try:
                with transaction.atomic():
                    bookschedule.valid = False
                    bookschedule.save()
                    records.booking_start_time = bookingStartTime
                    records.booking_end_time = bookingEndTime
                    records.teacher_id = teacherId
                    records.teacher_name = teacherName
                    records.teaching_type = teachingType
                    records.valid = True
                    records.save()

                    return JsonResponse({"message": "updated successfully."})
            except IntegrityError as e:
                return JsonResponse(
                    {"error": f"reason:{e}"},
                    status=400,
                )
        else:  # do not exist
            try:
                bookschedule = Booking_Schedule.objects.get(
                    booking_schedule_id=bookingScheduleId, order_id=orderId
                )
            except Booking_Schedule.DoesNotExist:
                return JsonResponse(
                    {"message": "booking schedule is not exist"}, status=400
                )
            try:
                with transaction.atomic():
                    bookschedule.valid = True
                    bookschedule.booking_start_time = bookingStartTime
                    bookschedule.booking_end_time = bookingEndTime
                    bookschedule.teacher_id = teacherId
                    bookschedule.teacher_name = teacherName
                    bookschedule.teaching_type = teachingType
                    bookschedule.save()

                    return JsonResponse({"message": "updated successfully."})
            except IntegrityError as e:
                return JsonResponse(
                    {"error": f"reason:{e}"},
                    status=400,
                )

    except Exception as e:
        return JsonResponse(
            {"message": f"udate schedule failed, reason:{e}"}, status=400
        )


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteBookingSchedule(request, account, orderId, bookingScheduleId):
    try:
        try:
            member = Member.objects.get(account=account)
            order = Order.objects.select_related("member").get(
                member=member, order_id=orderId
            )
            result = (
                Booking_Schedule.objects.select_related("member_id")
                .filter(
                    order=order,
                    booking_schedule_id=bookingScheduleId,
                    valid=True,
                )
                .values()
            )
            print(result)
            result = list(result)
            if len(result) == 0:
                raise Exception
        except Exception as e:
            return JsonResponse({"message": "Booking schedule not found"}, status=400)
        try:
            with transaction.atomic():
                bookschedule = Booking_Schedule.objects.get(
                    booking_schedule_id=bookingScheduleId
                )
                bookschedule.valid = False
                bookschedule.save()
                return JsonResponse({"message": "delete schedule sucessfully"})
        except Booking_Schedule.DoesNotExist:
            return JsonResponse({"message": "booking schedule not found"}, status=400)
    except Exception as e:
        return JsonResponse({"message": f"{e}"}, status=400)
