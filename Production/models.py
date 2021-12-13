from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from .choices import PROCESS_TYPE, STATE_PRODUCTION, CONSUMED, CORRECTION_TYPE
from Product.choices import TYPE_PRODUCT, PERFUMED


class Production(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(unique=False, blank=True, null=True)
    ref_code = models.CharField(max_length=250, blank=True, null=True)
    date = models.DateTimeField()
    product = models.ForeignKey(
        'Product.FinishedProductType', on_delete=models.SET_NULL, related_name="ProduitCible" , blank=True, null=True)
    coil_type =  models.ForeignKey(
        'Product.CoilType', on_delete=models.SET_NULL, related_name="BobineCible" , blank=True, null=True)
    coil = models.ForeignKey("Product.Coil", null=True, related_name="Bobine", blank=True, on_delete= models.CASCADE)
    quantity_produced = models.DecimalField(default =0, null=True,decimal_places=1, max_digits=5, blank=True)
    remaining = models.FloatField(null=True, blank=True)
    machine = models.ForeignKey(
        'Machine.Machine', on_delete=models.SET_NULL, blank=True, null=True)
    process_type = models.CharField(
        max_length=250, choices=PROCESS_TYPE, null=True, blank=True)
    state = models.CharField(
        max_length=250, choices=STATE_PRODUCTION, blank=True, null=True)
    color = models.ForeignKey(
        "Product.Color", on_delete=models.SET_NULL, verbose_name="Couleur", blank=True, null=True)
    mix_type = models.CharField(
        max_length=50, choices=TYPE_PRODUCT, null=True, blank=True)
    mix_perfume = models.CharField(
        max_length=50, blank=True, null=True, choices=PERFUMED)
    consumed = models.CharField(
        max_length=50, choices=CONSUMED, default="NOT_CONSUMED", blank=True, null=True)
    rectified = models.BooleanField("Rectifié", default=False, blank=True, null = True)

    def get_absolute_url(self):
        return reverse("production:", kwargs={"slug": self.slug})

    def __str__(self):
        get_color = self.color.name.upper() if self.color is not None else ""
        get_mix_remaining = self.remaining, self.quantity_produced,'kg' if self.remaining is not 0 and self.quantity_produced is not 0 else ""
        get_product = self.product.__str__().upper() if self.product is not None else ""
        get_coil_ref = self.coil.ref if self.coil is not None else ""
        if self.process_type == "MIXING":
            return f'{self.get_process_type_display()}-{self.id}{self.ref_code} {get_color} {self.get_mix_type_display()} {self.get_mix_perfume_display()} {get_mix_remaining}'
        elif self.process_type == "EXTRUSION" or self.process_type == "PRINTING" or self.process_type == "SHAPING":
            return f'{self.get_process_type_display()}-{self.id}{self.ref_code} ({get_coil_ref})'
        else:
            return f'{self.get_process_type_display()}-{self.id}{self.ref_code} ({get_product}__{self.quantity_produced}) '

    def save(self, *args, **kwargs):
        if self.process_type != "MIXING":
            self.ref_code = f'{self.id}{self.date.strftime("%m%d%y%s")}'
        if self.slug is None or self.slug == " ":
            tmp_slug = f'{self.get_process_type_display()}-{self.id}{self.date.strftime("%m%d%y%s")}'
            self.slug = slugify(tmp_slug)
        super(Production, self).save(*args, **kwargs)


    class Meta:
        verbose_name = 'Production'
        verbose_name_plural = 'Productions'
        db_table = 'Production'
        ordering = ["-date"]

class Cancellation(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL, blank=True, null=True)
    cancellation_type = models.CharField(max_length=255, blank=True, null=True)
    
    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            tmp_slug = f'{self.date}-{self.user}-{self.cancellation_type}'
            self.slug = slugify(tmp_slug)
        super(Cancellation, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.date}-{self.user}-{self.cancellation_type}'
    class Meta:
        verbose_name = 'Annulation Opération'
        verbose_name_plural = 'Annulations Opérations'
        db_table = 'Cancellation'
        ordering = ["-date"]

class HandleConsumption(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete= models.SET_NULL, related_name="handle_consumer", blank = True, null=True)
    handle = models.ForeignKey("Product.Handle",on_delete= models.SET_NULL, related_name="handle_consumed", blank=True, null=True)
    machine = models.ForeignKey("Machine.Machine", on_delete= models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name= "Nombre de rouleaux", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            tmp_slug = f'{self.date}-{self.quantity}'
            self.slug = slugify(tmp_slug)
        super(HandleConsumption, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.date}-{self.quantity}'
    class Meta:
        verbose_name = 'Consommation Cordon'
        verbose_name_plural = 'Consommations Cordon'
        db_table = 'HandleConsumption'
        ordering = ["-date"]

class LabellingConsumption(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete= models.SET_NULL, related_name="labelling_consumer", blank = True, null=True)
    labelling = models.ForeignKey("Product.Labelling",on_delete= models.SET_NULL, related_name="labelling_consumed", blank=True, null=True)
    machine = models.ForeignKey("Machine.Machine", on_delete= models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name= "Nombre d'étiquettes", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            tmp_slug = f'{self.date}-{self.quantity}'
            self.slug = slugify(tmp_slug)
        super(LabellingConsumption, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.date}-{self.quantity}'
    class Meta:
        verbose_name = 'Consommation Labelling'
        verbose_name_plural = 'Consommations Labelling'
        db_table = 'LabellingConsumption'
        ordering = ["-date"]

class PackageConsumption(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete= models.SET_NULL, related_name="package_consumer", blank = True, null=True)
    package = models.ForeignKey("Product.Package",on_delete= models.SET_NULL, related_name="package_consumed", blank=True, null=True)
    machine = models.ForeignKey("Machine.Machine", on_delete= models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(verbose_name= "Nombre d'unités", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            tmp_slug = f'{self.date}-{self.quantity}'
            self.slug = slugify(tmp_slug)
        super(PackageConsumption, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.date}-{self.quantity}'
    class Meta:
        verbose_name = 'Consommation Emballage'
        verbose_name_plural = 'Consommations Emballage'
        db_table = 'PackageConsumption'
        ordering = ["-date"]


class InkConsumption(models.Model):
    slug = models.SlugField(max_length=255, null=True, blank=True)
    date = models.DateTimeField(blank=True,null=True)
    user = models.ForeignKey(User,on_delete= models.SET_NULL, related_name="ink_consumer", blank = True, null=True)
    ink = models.ForeignKey("Product.RawMatter",on_delete= models.SET_NULL, related_name="ink_consumed", blank=True, null=True)
    machine = models.ForeignKey("Machine.Machine", on_delete= models.SET_NULL, blank=True, null=True)
    quantity = models.FloatField(verbose_name= "Quantité", null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == "":
            tmp_slug = f'{self.date}-{self.quantity}'
            self.slug = slugify(tmp_slug)
        super(InkConsumption, self).save(*args, **kwargs)
        
    def __str__(self):
        return f'{self.date}-{self.quantity}'
    class Meta:
        verbose_name = 'Consommation Encre'
        verbose_name_plural = 'Consommations Encre'
        db_table = 'InkConsumption'
        ordering = ["-date"]

class Correction(models.Model):
    slug = models.SlugField(unique=False, blank=True, null=True, max_length=255)
    date = models.DateField(blank=True, null = True)
    production = models.ForeignKey('Production', on_delete = models.SET_NULL, blank = True, null = True)
    difference = models.FloatField(verbose_name= "Ecart", null=True, blank=True)
    user = models.ForeignKey(User ,on_delete=models.SET_NULL, blank=True, null=True)
    type_difference = models.CharField("Type de l'écart", max_length=25 ,choices=CORRECTION_TYPE, blank=True, null = True)

    
    def __str__(self):
        return f'{self.production.user}-{self.difference}-{self.get_type_difference_display()}-{self.date}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super(Correction, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Correction'
        verbose_name_plural = 'Corrections'
        db_table = 'Correction'
        ordering = ["-date"]

class TrashCorrection(models.Model):
    slug = models.SlugField(max_length = 255, unique=False, blank=True, null=True)
    date = models.DateField(blank=True, null = True)
    trash = models.ForeignKey('Product.Trash', on_delete = models.SET_NULL, blank = True, null = True)
    difference = models.FloatField(verbose_name= "Ecart", null=True, blank=True)
    user = models.ForeignKey(User ,on_delete=models.SET_NULL, blank=True, null=True)
    type_difference = models.CharField("Type de l'écart", max_length=25 ,choices=CORRECTION_TYPE, blank=True, null = True)

    
    def __str__(self):
        get_user = self.trash.user if self.trash is not None else ''
        return f'{get_user}-{self.difference}-{self.get_type_difference_display()}-{self.date}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super(TrashCorrection, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Correction Déchet'
        verbose_name_plural = 'Corrections Déchet'
        db_table = 'Correction Déchet'
        ordering = ["-date"]

class GapRawMatter(models.Model):
    slug = models.SlugField(max_length = 255, unique=False, blank=True, null=True)
    date = models.DateField(blank=True, null = True)
    user = models.ForeignKey(User ,on_delete=models.SET_NULL, blank=True, null=True)
    rawmatter = models.ForeignKey('Product.RawMatter', on_delete = models.SET_NULL, blank = True, null = True)
    difference = models.FloatField(verbose_name= "Ecart", null=True, blank=True)
    type_difference = models.CharField("Type de l'écart", max_length=25 ,choices=CORRECTION_TYPE, blank=True, null = True)

    def __str__(self):
        return f'{self.user.first_name}-{self.user.last_name}-{self.rawmatter}-{self.difference}-{self.get_type_difference_display()}-{self.date}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super(GapRawMatter, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Correction Stock Atelier Matière Première'
        verbose_name_plural = 'Corrections Stock Atelier Matière Première'
        db_table = 'Correction Stock Atelier Matière Première'
        ordering = ["-date"]

class GapHandle(models.Model):
    slug = models.SlugField(max_length = 255, unique=False, blank=True, null=True)
    date = models.DateField(blank=True, null = True)
    user = models.ForeignKey(User ,on_delete=models.SET_NULL, blank=True, null=True)
    handle = models.ForeignKey('Product.Handle', on_delete = models.SET_NULL, blank = True, null = True)
    difference = models.FloatField(verbose_name= "Ecart", null=True, blank=True)
    type_difference = models.CharField("Type de l'écart", max_length=25 ,choices=CORRECTION_TYPE, blank=True, null = True)

    def __str__(self):
        return f'{self.user.first_name}-{self.user.last_name}-{self.handle}-{self.difference}-{self.get_type_difference_display()}-{self.date}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super(GapHandle, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Correction Stock Atelier Cordon'
        verbose_name_plural = 'Corrections Stock Atelier Cordon'
        db_table = 'Correction Stock Atelier Cordon'
        ordering = ["-date"]

class GapLabelling(models.Model):
    slug = models.SlugField(max_length = 255, unique=False, blank=True, null=True)
    date = models.DateField(blank=True, null = True)
    user = models.ForeignKey(User ,on_delete=models.SET_NULL, blank=True, null=True)
    labelling = models.ForeignKey('Product.Labelling', on_delete = models.SET_NULL, blank = True, null = True)
    difference = models.FloatField(verbose_name= "Ecart", null=True, blank=True)
    type_difference = models.CharField("Type de l'écart", max_length=25 ,choices=CORRECTION_TYPE, blank=True, null = True)

    def __str__(self):
        return f'{self.user.first_name}-{self.user.last_name}-{self.labelling}-{self.difference}-{self.get_type_difference_display()}-{self.date}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super(GapLabelling, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Correction Stock Atelier Labelling'
        verbose_name_plural = 'Corrections Stock Atelier Labelling'
        db_table = 'Correction Stock Atelier Labelling'
        ordering = ["-date"]

class GapPackage(models.Model):
    slug = models.SlugField(max_length = 255, unique=False, blank=True, null=True)
    date = models.DateField(blank=True, null = True)
    user = models.ForeignKey(User ,on_delete=models.SET_NULL, blank=True, null=True)
    package = models.ForeignKey('Product.Package', on_delete = models.SET_NULL, blank = True, null = True)
    difference = models.FloatField(verbose_name= "Ecart", null=True, blank=True)
    type_difference = models.CharField("Type de l'écart", max_length=25 ,choices=CORRECTION_TYPE, blank=True, null = True)

    def __str__(self):
        return f'{self.user.first_name}-{self.user.last_name}-{self.package}-{self.difference}-{self.get_type_difference_display()}-{self.date}'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())
        super(GapPackage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Correction Stock Atelier Emballage'
        verbose_name_plural = 'Corrections Stock Atelier Emballage'
        db_table = 'Correction Stock Atelier Emballage'
        ordering = ["-date"]
