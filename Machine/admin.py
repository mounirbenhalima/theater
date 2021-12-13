from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Machine, MachineType, MachineStop


admin.site.register(Machine)
admin.site.register(MachineStop)
admin.site.register(MachineType)
