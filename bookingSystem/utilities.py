from django import forms


class addBookingScheduleForm(forms.Form):
    account = forms.EmailField()
    orderId = forms.IntegerField()
    teacherName = forms.CharField(max_length=100)
    teacherId = forms.IntegerField()
    teachingType = forms.IntegerField()


class registerForm(forms.Form):
    account = forms.EmailField()
    firstName = forms.CharField()
    lastName = forms.CharField()
    hitutorAccount = forms.CharField()
    hitutorPassword = forms.CharField()
    emailAddress = forms.CharField()


class addOrderForm(forms.Form):
    account = forms.EmailField()
    purchaseOrderId = forms.IntegerField()
    lessonId = forms.IntegerField()
