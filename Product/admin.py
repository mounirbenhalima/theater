from django.contrib import admin

from Product.models import Ticket, TicketSale

from django.forms import CheckboxSelectMultiple
from django.db import models

admin.site.register(Ticket)
admin.site.register(TicketSale)