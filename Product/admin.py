from django.contrib import admin

from Product.models import (
    Brand,
    Color,
    Product,
    Coil,
    RawMatter,
    Range,
    CombinedRange,
    FinishedProduct,
    FinishedProductType,
    CoilType,
    Trash,
    Handle,
    Labelling,
    Package,
    SparePart

)

from django.forms import CheckboxSelectMultiple
from django.db import models

admin.site.register(CoilType)
admin.site.register(Coil)
admin.site.register(FinishedProduct)


admin.site.register(Range)
admin.site.register(CombinedRange)

admin.site.register(FinishedProductType)

admin.site.register(RawMatter)
admin.site.register(Brand)
admin.site.register(Color)
admin.site.register(Product)
admin.site.register(Trash)
admin.site.register(Handle)
admin.site.register(Labelling)
admin.site.register(Package)
admin.site.register(SparePart)