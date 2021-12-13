from django.contrib import admin
from .models import Warehouse, Order,OrderItem,OrderHandle,OrderLabelling, TrashOut, OrderSparePart, Loss, SparePartConsumption, CoilSale

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(OrderHandle)
admin.site.register(OrderLabelling)
admin.site.register(OrderSparePart)
admin.site.register(SparePartConsumption)
admin.site.register(CoilSale)

admin.site.register(Warehouse)

admin.site.register(TrashOut)
admin.site.register(Loss)