from django.db import models
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db.models import Q
from Product.models import Coil

CONTACT_TYPE = (
    ('SUPPLIER', 'Fournisseur'),
    ('CLIENT', 'Client'),
    ('WORKSHOP', 'Atelier'),
)
REGION = (
    ('ORAN', 'Oran'),
)

class Contact(models.Model):
    slug = models.SlugField(max_length=255)
    last_name = models.CharField(
        "Nom de Famille", max_length=200, null=True, blank=True)
    first_name = models.CharField(
        "Prénom", max_length=200, null=True, blank=True)
    email = models.EmailField(blank=True, null=True)
    phone_number = models.CharField(
        'Numero de Téléphone', max_length=10, blank=True, null=True)
    contact_type = models.CharField(
        'Type de Contact', choices=CONTACT_TYPE, max_length=25, blank=True, null=True)
    address = models.CharField(
        "Adresse", max_length=255, blank=True, null=True)

    region = models.CharField(
        "Wilaya", max_length=255, choices=REGION, blank=True, null=True
    )
    def get_absolute_url(self):
        return reverse("contact:update-contact", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("contact:delete-contact", kwargs={"slug": self.slug})

    def __str__(self):
        get_contact_type = self.get_contact_type_display() if self.contact_type is not None else ''
        return f'{self.id}-{self.first_name} {self.last_name} - {get_contact_type}'

    def save(self, *args, **kwargs):
        get_contact_type = self.get_contact_type_display() if self.contact_type is not None else ''

        self.slug = slugify(f'{self.id} {self.first_name} {self.last_name} - {get_contact_type}')

        super(Contact, self).save(*args, **kwargs)

    def number_sold(self, start_date, end_date):
        orders = self.Clients.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(type_order = "STOCK_OUT"))
        total = 0
        for o in orders:
            for i in o.items.all():
                total += i.quantity
        
        return total
    
    def weight_sold(self, start_date, end_date):
        orders = self.Clients.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(type_order = "STOCK_OUT"))
        total = 0
        for o in orders:
            for i in o.items.all():
                total += i.quantity * i.item.weight
        
        return total

    def extrusion_number(self, start_date, end_date):
        coils = Coil.objects.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(supplier = self))
        total = coils.count()
        
        return total
    
    def extrusion_weight(self, start_date, end_date):
        coils = Coil.objects.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(supplier = self))
        total = 0
        for c in coils:
            total += c.weight
        
        return total

    def defective_number(self, start_date, end_date):
        coils = Coil.objects.exclude(status = "CUT").filter(Q(supplier = self) & Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(defective = "DEFECTIVE"))
        total = coils.count()
        
        return total

    def defective_weight(self, start_date, end_date):
        coils = Coil.objects.exclude(status = "CUT").filter(Q(supplier = self) & Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(defective = "DEFECTIVE"))
        total = 0
        for c in coils:
            total += c.weight
        
        return total

    def quarantine_number(self, start_date, end_date):
        coils = Coil.objects.exclude(status = "CUT").filter(Q(supplier = self) & Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(status = "QUARANTINE"))
        total = coils.count()
        
        return total

    def quarantine_weight(self, start_date, end_date):
        coils = Coil.objects.exclude(status = "CUT").filter(Q(supplier = self) & Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(status = "QUARANTINE"))
        total = 0
        for c in coils:
            total += c.weight
        
        return total

    def destroy_number(self, start_date, end_date):
        coils = Coil.objects.exclude(status = "CUT").filter(Q(supplier = self) & Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(status = "TO_BE_DESTROYED"))
        total = coils.count()
        
        return total

    def destroy_weight(self, start_date, end_date):
        coils = Coil.objects.exclude(status = "CUT").filter(Q(supplier = self) & Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(status = "TO_BE_DESTROYED"))
        total = 0
        for c in coils:
            total += c.weight
        
        return total

    class Meta:
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'
        db_table = 'Contact'
        ordering = ['contact_type']
