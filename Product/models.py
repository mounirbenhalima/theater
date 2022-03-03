from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.utils.crypto import get_random_string

from django.db.models import Q
from decimal import Decimal

from django.core.validators import MinValueValidator
from django.contrib.auth.models import User

class Ticket(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=255)
    ref = models.CharField("Référence", max_length=255, blank=True, null=True)
    price = models.FloatField("Tarif", default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        get_ref = self.ref if self.ref is not None else ''
        get_price = self.price if self.price is not None else ''

        slug_ticket = f"ticket-{get_ref}-{get_price}"
        if self.slug is None:
            self.ref = get_random_string(5)
            self.slug = slugify(slug_ticket)
        super(Ticket, self).save(*args, **kwargs)

    def __str__(self):
        get_ref = self.ref if self.ref is not None else ''
        get_price = self.price if self.price is not None else ''
        return f"Ticket-{get_ref} - {get_price} DA"
    
    def sales_number(self, start_date, end_date):
        sales = TicketSale.objects.filter(Q(date__lte = end_date) & Q(date__gte = start_date) & Q(ticket = self))
        total = 0
        total = sales.count()
        
        return total
    
    def sales_value(self, start_date, end_date):
        sales = TicketSale.objects.filter(Q(date__lte = end_date) & Q(date__gte = start_date) & Q(ticket = self))
        total = 0
        for i in sales:
            total += i.price
        
        return total
        
    def get_absolute_url(self):
        return reverse("product:ticket-update", kwargs={"slug": self.slug})
    def get_delete_url(self):
        return reverse("product:ticket-delete", kwargs={"slug": self.slug})

class TicketSale(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=255)
    ref = models.CharField("Référence", max_length=255, blank=True, null=True)
    date = models.DateTimeField()
    ticket = models.ForeignKey('Ticket', on_delete=models.SET_NULL, blank=True, null=True)
    price = models.FloatField("Tarif", default=0, null=True, blank=True)

    def save(self, *args, **kwargs):
        get_ticket = self.ticket.ref if self.ticket is not None else ''
        get_ref = self.ref if self.ref is not None else ''
        get_price = self.price if self.price is not None else ''

        slug_sale = f"sale-{self.date}-{get_ticket}-{get_ref}-{get_price}"
        if self.slug is None:
            self.ref = get_random_string(5)
            self.slug = slugify(slug_sale)
        super(TicketSale, self).save(*args, **kwargs)

    def __str__(self):
        get_ticket = self.ticket.ref if self.ticket is not None else ''
        get_ref = self.ref if self.ref is not None else ''
        get_price = self.price if self.price is not None else ''
        return f"Ticket-{self.date} {get_ref} - {get_price} DA"