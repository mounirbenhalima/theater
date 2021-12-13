from django.contrib import admin
from .models import Production, Correction, TrashCorrection, GapRawMatter, GapHandle, GapLabelling, GapPackage, Cancellation, HandleConsumption, LabellingConsumption, PackageConsumption, InkConsumption
# from import_export.admin import ImportExportModelAdmin


admin.site.register(Production)
admin.site.register(InkConsumption)
admin.site.register(Correction)
admin.site.register(HandleConsumption)
admin.site.register(LabellingConsumption)
admin.site.register(PackageConsumption)
admin.site.register(TrashCorrection)
admin.site.register(GapRawMatter)
admin.site.register(GapHandle)
admin.site.register(GapLabelling)
admin.site.register(GapPackage)
admin.site.register(Cancellation)