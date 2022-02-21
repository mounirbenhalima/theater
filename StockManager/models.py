from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
import datetime
from django.utils.text import slugify
from django.shortcuts import get_object_or_404
from .choices import STOCK_PROCESS, STOCK, CONSUMPTION_TYPE, LOSS_TYPE, INTERVENTION_TYPE
from Product.choices import TYPE_TRASH


class TrashOut(models.Model):
    slug = models.SlugField (max_length = 255, blank=True, null=True)
    date = models.DateField("Date")
    ref = models.CharField("Référence", max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete= models.SET_NULL, blank=True, null=True)
    trash_type = models.CharField("Type de déchet", max_length=255, blank=True, null=True, choices=TYPE_TRASH)
    weight = models.FloatField("Poids", null=True, blank=True)
    destination = models.ForeignKey('Company.company', null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        get_date = self.date if self.date is not None else ""
        get_ref = self.ref if self.ref is not None else ""
        get_user = self.user if self.user is not None else ""
        get_trash_type = self.get_trash_type_display() if self.get_trash_type_display() is not None else ""
        get_weight = self.weight if self.weight is not None else ""
        get_destination = self.destination if self.destination is not None else ""
        return f'{get_date} {get_ref} {get_user} {get_trash_type} {get_weight}Kg {get_destination}'

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.__str__())

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-date"]


class Warehouse(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.name


class OrderItem(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user_loged",
                             blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        'Product.Product', on_delete=models.CASCADE, related_name='product_id')
    quantity = models.IntegerField(blank=True, null=True)
    reminder = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, null = True, blank=True)

    def __str__(self):
        return f'{self.quantity} de {self.item.product_designation}'

class OrderHandle(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user_logged",
                             blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        'Product.Handle', on_delete=models.CASCADE, related_name='handle_id')
    quantity = models.IntegerField(blank=True, null=True)
    reminder = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, null = True, blank=True)

    def __str__(self):
        return f'{self.item}'

class OrderLabelling(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user_loggged",
                             blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        'Product.Labelling', on_delete=models.CASCADE, related_name='labelling_id')
    quantity = models.IntegerField(blank=True, null=True)
    reminder = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, null = True, blank=True)

    def __str__(self):
        return f'{self.item}'

class OrderPackage(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user_logggged",
                             blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        'Product.Package', on_delete=models.CASCADE, related_name='package_id')
    quantity = models.IntegerField(blank=True, null=True)
    reminder = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, null = True, blank=True)

    def __str__(self):
        return f'{self.item}'

class OrderTape(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user_loggggged",
                             blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        'Product.Tape', on_delete=models.CASCADE, related_name='tape_id')
    quantity = models.IntegerField(blank=True, null=True)
    reminder = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, null = True, blank=True)

    def __str__(self):
        return f'{self.item}'

class OrderSparePart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="user_logggggged",
                             blank=True, null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(
        'Product.SparePart', on_delete=models.CASCADE, related_name='part_id')
    quantity = models.IntegerField(blank=True, null=True)
    reminder = models.IntegerField(blank=True, null=True)
    identifier = models.CharField(max_length=255, null = True, blank=True)

    def __str__(self):
        return f'{self.item}'

class SparePartConsumption(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete= models.SET_NULL, related_name="spare_part_consumer", blank = True, null=True)
    part = models.ForeignKey("Product.SparePart",on_delete= models.SET_NULL, related_name="spare_part_consumed", blank=True, null=True)
    machine = models.ForeignKey("Machine.Machine", on_delete= models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name= "Nombre d'Unités", null=True, blank=True)
    intervention_type = models.CharField(max_length=255, null = True, blank=True, choices= INTERVENTION_TYPE)
    
    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            tmp_slug = f'{self.date}-{self.part}-{self.quantity}'
            self.slug = slugify(tmp_slug)
        super(SparePartConsumption, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.date}-{self.quantity}'
    class Meta:
        verbose_name = 'Consommation Pièce de Rechange'
        verbose_name_plural = 'Consommations Pièces de Rechange'
        db_table = 'SparePartConsumption'
        ordering = ["-date"]

class Order(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             related_name="user_id",
                             blank=True, null=True)
    supplier = models.ForeignKey("Contact.Contact", related_name="Fournisseurs",
                                on_delete=models.SET_NULL, default=None, blank=True, null=True)
    intern_user = models.ForeignKey(User,on_delete=models.SET_NULL,default=None, null=True, blank=True)
    client = models.ForeignKey("Contact.Contact", related_name="Clients" ,on_delete = models.SET_NULL,default=None, blank=True, null=True)
    company = models.ForeignKey("Company.Company", blank=True, null=True, on_delete = models.SET_NULL)
    ref_code = models.CharField(max_length=20, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, unique=False)
    items = models.ManyToManyField(OrderItem, blank=True, null=True)
    handles = models.ManyToManyField(OrderHandle, blank=True, null = True)
    labellings = models.ManyToManyField(OrderLabelling, blank = True, null = True)
    packages = models.ManyToManyField(OrderPackage, blank = True, null = True)
    tapes = models.ManyToManyField(OrderTape, blank = True, null = True)
    parts = models.ManyToManyField(OrderSparePart, blank = True, null = True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    type_order = models.CharField(
        max_length=25, blank=True, null=True, choices=STOCK_PROCESS)
    type_consumption = models.CharField(
        max_length=25, blank=True, null=True, choices=CONSUMPTION_TYPE)

    category = models.CharField('Catégorie', max_length=255, null = True, blank= True)
    external_stock = models.BooleanField(default=False)
    machine = models.ForeignKey("Machine.Machine", on_delete=models.SET_NULL,blank=True, null=True, default=None)

    def __str__(self):
        return f'{self.ref_code}'

    def get_total(self):
        total = 0
        if self.category == "Matière Première" or self.category == "Produit Fini":
            for item in self.items.all():
                total += item.quantity
        elif self.category == "Cordon":
            for item in self.handles.all():
                total += item.quantity
        elif self.category == "Labelling":
            for item in self.labellings.all():
                total += item.quantity
        elif self.category == "Emballage":
            for item in self.packages.all():
                total += item.quantity
        elif self.category == "Scotch":
            for item in self.tapes.all():
                total += item.quantity
        elif self.category == "Pièce de Rechange":
            for item in self.parts.all():
                total += item.quantity
        return total
    
    def get_amount(self):
        total = 0
        if self.category == "Matière Première" or self.category == "Produit Fini":
            for item in self.items.all():
                total += item.quantity * item.item.price
        elif self.category == "Cordon":
            for item in self.handles.all():
                total += item.quantity * item.item.price
        elif self.category == "Labelling":
            for item in self.labellings.all():
                total += item.quantity * item.item.price
        elif self.category == "Emballage":
            for item in self.packages.all():
                total += item.quantity * item.item.price
        elif self.category == "Scotch":
            for item in self.tapes.all():
                total += item.quantity * item.item.price
        elif self.category == "Pièce de Rechange":
            for item in self.parts.all():
                total += item.quantity * item.item.price
        return total

    def get_absolute_url(self):
        return reverse("stock-manager:order-detail", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("stock-manager:order-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        get_day = datetime.date.today().strftime("%m%d%y")
        if self.ref_code is None and self.id is not None:
            self.ref_code = get_slug = f'{get_day}-{self.user.id}{self.id}'
            self.slug = get_slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-ordered_date"]

class Loss(models.Model):
    slug = models.SlugField(max_length = 255, unique=False, blank=True, null=True)
    date = models.DateField(blank=True, null = True)
    user = models.ForeignKey(User ,on_delete=models.SET_NULL, blank=True, null=True)
    rawmatter = models.ForeignKey('Product.RawMatter', on_delete = models.SET_NULL, blank = True, null = True)
    labelling = models.ForeignKey('Product.Labelling', on_delete = models.SET_NULL, blank = True, null = True)
    package = models.ForeignKey('Product.Package', on_delete = models.SET_NULL, blank = True, null = True)
    quantity = models.FloatField(verbose_name= "Quantité", null=True, blank=True)
    loss_type = models.CharField(max_length=255, blank=True, choices=LOSS_TYPE , null=True)
    cause = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        get_rawmatter = self.rawmatter if self.rawmatter is not None else ''
        get_labelling = self.labelling if self.labelling is not None else ''
        get_package = self.package if self.package is not None else ''
        if self.rawmatter is not None:
            return f'Perte MP {self.date}-{self.user}-{get_rawmatter}-{self.quantity}'
        elif self.labelling is not None:
            return f'Perte Labelling {self.date}-{self.user}-{get_labelling}-{self.quantity}'
        elif self.package is not None:
            return f'Perte Emballage {self.date}-{self.user}-{get_package}-{self.quantity}'
        else:
            return f'Perte {self.date}-{self.user}-{self.quantity}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super(Loss, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Perte'
        verbose_name_plural = 'Pertes'
        db_table = 'Perte'
        ordering = ["-date"]

class CoilSale(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete= models.SET_NULL, related_name="coil_saler", blank = True, null=True)
    coil = models.ForeignKey("Product.Coil",on_delete= models.SET_NULL, related_name="coil_sold", blank=True, null=True)
    client = models.ForeignKey("Contact.Contact", on_delete= models.SET_NULL, blank=True, null=True)
    
    
    def save(self, *args, **kwargs):
        tmp_slug = f'{self.date}-{self.coil}'
        self.slug = slugify(tmp_slug)
        super(CoilSale, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.date}-{self.coil}'
        
    class Meta:
        verbose_name = 'Vente Bobine'
        verbose_name_plural = 'Ventes Bobines'
        db_table = 'CoilSale'
        ordering = ["-date"]