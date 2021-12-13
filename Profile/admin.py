from django.contrib import admin

from .models import Profile,JobPosition, HolidayRequest, Point, Salary

admin.site.register(Profile)
admin.site.register(JobPosition)
admin.site.register(HolidayRequest)
admin.site.register(Point)
admin.site.register(Salary)