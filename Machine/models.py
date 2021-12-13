from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.template.defaultfilters import slugify
from .choices import MACHINE_STATE, MACHINE_STOP
from Product.choices import TYPE_PRODUCT, PERFUMED


class MachineType(models.Model):
    name = models.CharField(blank=True, null=True,
                            max_length=200, verbose_name="Type de la machine")

    slug = models.SlugField(unique=True)

    def __str__(self):
        return f'{self.name}'

    def get_machine_type_url(self):
        return reverse("machine:machinetype-add",
                       kwargs={
                           "slug": self.slug
                       })

    def get_absolute_url(self):
        return reverse("machine:machinetype-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("machine:machinetype-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not MachineType.objects.filter(slug=self.slug).exists():
            _slug = f"{self.id} {self.name}"
            self.slug = slugify(_slug)

        super(MachineType, self).save(*args, **kwargs)
    
    class Meta:
        ordering = ['name']


class MachineStop(models.Model):
    slug = models.SlugField(unique=False, blank=True, null=True, max_length=255)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    date = models.DateTimeField()
    machine = models.ForeignKey('Machine', on_delete=models.SET_NULL, blank=True, null=True)
    hours = models.IntegerField(null=True, blank=True, default=0)
    minutes = models.IntegerField(null=True, blank=True, default=0)
    duration = models.IntegerField(null=True, blank=True, default=0)
    cause = models.CharField(max_length=250,choices=MACHINE_STOP, null=True, blank=True)
    comment = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}-{self.machine.designation}-{self.hours}:{self.minutes}-{self.get_cause_display()}'

    def save(self, *args, **kwargs):
        self.duration = self.hours * 60 + self.minutes
        if self.slug is None or self.slug == " ":
            tmp_slug = f'{self.date}{self.machine.designation}-{self.hours}{self.minutes}-{self.cause}'
            self.slug = slugify(tmp_slug)
        super(MachineStop, self).save(*args, **kwargs)


class Machine(models.Model):
    model_name = models.CharField(
        blank=True, null=True, max_length=200, verbose_name="Modèle")
    slug = models.SlugField(unique=True)
    brand = models.ForeignKey(
        "Product.Brand", on_delete=models.SET_NULL, null=True, blank=True)
    machine_type = models.ForeignKey(
        "MachineType", on_delete=models.SET_NULL, null=True, blank=True)
    machine_number = models.PositiveIntegerField(
        "Numéro", null=True, blank=True)
    state = models.CharField(
        "Etat de la machine", max_length=250, choices=MACHINE_STATE, default="FREE", null=True, blank=True)
    designation = models.CharField(max_length=255, blank=True, null=True)

    def get_absolute_url(self):
        return reverse("machine:machine-update", kwargs={"slug": self.slug})
    
    def get_free_url(self):
        return reverse("machine:machine-free", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("machine:machine-delete", kwargs={"slug": self.slug})

    def __str__(self):
        get_brand = self.brand.name if self.brand != None else " "
        get_model_name = self.model_name if self.model_name != None else " "
        get_machine_type = self.machine_type if self.machine_type != None else " "
        get_machine_number = self.machine_number if self.machine_number != None else int(0)
        _str = f"{get_machine_type}-N°{get_machine_number} [{get_brand}-{get_model_name}]"
        return _str

    def save(self, *args, **kwargs):
        if not Machine.objects.filter(slug=self.slug).exists():
            get_id = self.id
            get_brand = self.brand.name if self.brand != None else " "
            get_model_name = self.model_name if self.model_name != None else " "
            get_machine_type = self.machine_type if self.machine_type != None else " "
            get_machine_number = self.machine_number if self.machine_number != None else int(0)
            _slug = f"{get_id} {get_machine_type} {get_brand} {get_model_name} {get_machine_number}"
            self.designation = self.__str__()
            self.slug = slugify(_slug)

        super(Machine, self).save(*args, **kwargs)

    def extrusion_number(self, start_date, end_date):
        coils = self.extrudeuse.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date))
        total = 0
        total = coils.count()
        
        return total

    def extrusion_weight(self, start_date, end_date):
        coils = self.extrudeuse.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date))
        total = 0
        for p in coils:
            total += p.weight
        
        return total

    def printing_number(self, start_date, end_date):
        coils = self.imprimeuse.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date))
        total = 0
        total = coils.count()
        
        return total

    def printing_weight(self, start_date, end_date):
        coils = self.imprimeuse.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date))
        total = 0
        for p in coils:
            total += p.weight
        
        return total

    
    def shaping_number(self, start_date, end_date):
        coils = self.soudeuse.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date))
        total = 0
        total = coils.count()
        
        return total

    def shaping_weight(self, start_date, end_date):
        coils = self.soudeuse.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date))
        total = 0
        for p in coils:
            total += p.weight
        
        return total

    def production_number(self, start_date, end_date):
        productions = self.production_set.filter(Q(date__lte = end_date) & Q(date__gte = start_date) & Q(process_type = "FINISHED_PRODUCT"))
        total = 0
        for i in productions:
            total += i.quantity_produced

        return total

    def production_weight(self, start_date, end_date):
        productions = self.production_set.filter(Q(date__lte = end_date) & Q(date__gte = start_date) & Q(process_type = "FINISHED_PRODUCT"))
        total = 0
        for i in productions:
            total += i.quantity_produced * i.product.weight
            
        return total
        

    def trash_weight(self, start_date, end_date):
        trash = self.trash_set.filter(Q(date__lte = end_date) & Q(date__gte = start_date))
        total = 0
        for t in trash:
            total += t.weight
        
        return total
    
    class Meta:
        ordering = ['machine_type', 'machine_number']