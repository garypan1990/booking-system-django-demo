from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    # ex: /polls/
    # path("", views.index, name="index"),
    path("", TemplateView.as_view(template_name="index.html")),
    # ex: /polls/5/
    path("memberList/", views.memberList, name="memberList"),
    path("register/", views.register, name="register"),
    path("addOrder/", views.addOrder, name="addOrder"),
    path(
        "deleteOrder/<str:account>/<int:orderId>", views.deleteOrder, name="deleteOrder"
    ),
    path("getBookSchedule/", views.getBookSchedule, name="getBookSchedule"),
    path("addBookSchedule/", views.addBookSchedule, name="addBookSchedule"),
    path("updateBookSchedule/", views.updateBookSchedule, name="updateBookSchedule"),
    path(
        "deleteBookSchedule/<str:account>/<int:orderId>/<int:bookingScheduleId>",
        views.deleteBookingSchedule,
        name="deleteBookingSchedule",
    ),
]
