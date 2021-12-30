from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify

from django.db.models import Q

from django.core.validators import MinValueValidator
from .choices import SIZE, RANGE_CATEGORY, TYPE_TRASH,TAPE_TYPE, PRINT_CHOICES, TYPE_PRODUCT, TYPE_PIECE, PERFUMED, COIL_STATUS, DEFECTIVE_CHOICES, PRINTED, TRASH_STATE
from django.contrib.auth.models import User
from Production.models import Production
from StockManager.models import Order, SparePartConsumption


class Brand(models.Model):
    name = models.CharField(
        "Marque",
        max_length=200,
        unique=True
    )
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product:brand-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("product:brand-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        super(Brand, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Marque'
        verbose_name_plural = 'Marques'
        db_table = 'Brand'
        ordering = ['id']

class Color(models.Model):
    name = models.CharField(
        "Couleur",
        max_length=200,
        unique=True,
    )

    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("product:color-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("product:color-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)
        super(Color, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Couleur'
        verbose_name_plural = 'Couleurs'
        db_table = 'Color'
        ordering = ["id"]

class Flavor(models.Model):
    name = models.CharField(
        "Parfum",
        max_length=200,
        unique=True,
    )

    slug = models.SlugField(unique=True)

    def get_absolute_url(self):
        return reverse("product:flavor-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("product:flavor-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Flavor, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Parfum'
        verbose_name_plural = 'Parfums'
        ordering = ["name"]

class Range(models.Model):
    slug = models.SlugField(unique=False)
    name = models.CharField(max_length=255, null=True, blank=True)
    

    def get_absolute_url(self):
        return reverse("product:range-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("product:range-delete", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.name}"

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        self.slug = slugify(self.name)

        super(Range, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Gamme'
        verbose_name_plural = 'Gammes'
        db_table = 'Range'
        ordering = ['id']


class Product(models.Model):
    name = models.ForeignKey(
        'Range', on_delete=models.SET_NULL, blank=True, null=True)
    combined_range = models.ForeignKey(
        'CombinedRange', on_delete=models.SET_NULL, blank=True, null=True)
    slug = models.SlugField(unique=False, blank=True,
                            null=True, max_length=255)
    ref = models.CharField(max_length=200, null=True, blank=True)
    product_designation = models.CharField(max_length=200, null=True, blank=True)
    weight = models.DecimalField(default =0, null=True,decimal_places=1, max_digits=5, blank=True)
    quantity = models.IntegerField("Quantité", default=0, blank=True, null=True)
    quantity_workshop = models.IntegerField("Quantité dans l'atelier", default=0, blank=True, null=True)
    external_quantity = models.IntegerField("Stock Externe", default=0, blank=True, null=True)
    threshold = models.PositiveIntegerField("Seuil", default=0, blank=True, null=True)
    price = models.FloatField('Prix', null=True, blank=True)
    type_name = models.CharField(max_length=250, choices=TYPE_PRODUCT, null=True, blank=True)

    perfume = models.CharField(max_length=250, blank=True, null=True, choices=PERFUMED)

    flavor = models.ForeignKey('Flavor', on_delete=models.SET_NULL, blank=True, null= True)

    warehouse = models.ForeignKey("StockManager.Warehouse", on_delete=models.SET_NULL, verbose_name="Entrepot", blank=True, null=True)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE, verbose_name="Marque", blank=True, null=True)
    color = models.ForeignKey("Color", on_delete=models.CASCADE, verbose_name="Couleur", blank=True, null=True)
    flavor = models.ForeignKey("Flavor", on_delete=models.CASCADE, verbose_name="Parfum", blank=True, null=True)

    def get_delete_url(self):
        return reverse("product:product-delete", kwargs={"slug": self.slug})

    def get_add_to_order_url(self):
        return reverse("stock-manager:add-to-order", kwargs={"slug": self.slug})

    def __str__(self):
        return f"{self.slug}"

    class Meta:
        verbose_name = 'Produit'
        verbose_name_plural = 'Produits'
        db_table = 'Product'
        ordering = ['name__name', 'brand__name']


class CombinedRange(models.Model):
    slug = models.SlugField(unique=False, blank=True, null=True, max_length=255)

    range_name = models.ForeignKey('Range', on_delete=models.SET_NULL, blank=True, null=True)

    capacity = models.CharField("Taille",max_length=255, blank=True, null=True)

    the_print = models.CharField("Impression", max_length=250, choices=PRINT_CHOICES, null=True, blank=True)

    perfume = models.CharField(max_length=250, blank=True, null=True, choices=PERFUMED)

    color = models.ForeignKey("Color", on_delete=models.CASCADE, verbose_name="Couleur", blank=True, null=True)

    type_name = models.CharField(max_length=250, choices=TYPE_PRODUCT, null=True, blank=True)

    category = models.CharField(max_length=250, choices=RANGE_CATEGORY, null=True, blank=True)

    def get_absolute_url(self):
        return reverse("product:c-range-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("product:c-range-delete", kwargs={"slug": self.slug})

    def __str__(self):
        get_range_name = self.range_name if self.range_name is not None else ""
        get_capacity = self.get_capacity_display() if self.capacity is not None else ""
        get_print = self.get_the_print_display() if self.the_print is not None else ""
        get_type_name = self.get_type_name_display() if self.type_name is not None else ""
        get_color = self.color if self.color is not None else ""
        get_perfume = self.get_perfume_display() if self.perfume is not None else ""
        if self.category == "FINAL_PRODUCT":
            return f"{get_range_name} {get_capacity} ({get_print}) {get_perfume}"
        elif self.category == "RAW_MATTER":
            return f"{get_range_name} {get_type_name} {get_color} {get_perfume}"
        else:
            return f"{get_range_name} {get_type_name}"

    def save(self, *args, **kwargs):
        self.slug = slugify(self.__str__())

        super(CombinedRange, self).save(*args, **kwargs)

    def black_quantity_produced(self, start_date, end_date):
        productions = Production.objects.filter(Q(date__lte = end_date) & Q(date__gte = start_date) & Q(product__combined_range = self) & Q(product__color__name = "noir"))
        total = 0
        for p in productions:
            if p.quantity_produced is not None:
                total += p.quantity_produced
        
        return total
    
    def color_quantity_produced(self, start_date, end_date):
        productions = Production.objects.exclude(Q(product__color__name = "noir")).filter(Q(date__lte = end_date) & Q(date__gte = start_date) & Q(product__combined_range = self))
        total = 0
        for p in productions:
            if p.quantity_produced is not None:
                total += p.quantity_produced
        
        return total

    def black_quantity_sold(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(type_order = "STOCK_OUT") & Q(category = "Produit Fini"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item.combined_range == self and i.item.color.name == "noir":
                    total += i.quantity
        
        return total
    
    def color_quantity_sold(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(type_order = "STOCK_OUT") & Q(category = "Produit Fini"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item.combined_range == self and i.item.color.name != "noir":
                    total += i.quantity
        
        return total

    def quantity_mixed(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(user__profile__job_position__name = "Mélangeur"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item.combined_range == self:
                    total += i.quantity
        
        return total
    
    def quantity_bought(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(type_order = "STOCK_ENTRY") & Q(category = "Matière Première"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item.combined_range == self:
                    total += i.quantity
        
        return total

    def product_main_stock(self, start_date, end_date):
        products = FinishedProductType.objects.filter(Q(combined_range = self))
        total = 0
        for p in products:
            if p.quantity is not None:
                total += p.quantity
        
        return total
    
    def product_external_stock(self, start_date, end_date):
        products = FinishedProductType.objects.filter(Q(combined_range = self))
        total = 0
        for p in products:
            if p.quantity is not None:
                total += p.external_quantity
        
        return total
    
    def raw_main_stock(self, start_date, end_date):
        products = RawMatter.objects.filter(Q(combined_range = self))
        total = 0
        for p in products:
            if p.quantity is not None:
                total += p.quantity
        
        return total

    def raw_workshop_stock(self, start_date, end_date):
        products = RawMatter.objects.filter(Q(combined_range = self))
        total = 0
        for p in products:
            if p.quantity is not None:
                total += p.quantity_workshop
        
        return total

    class Meta:
        ordering = ['range_name', 'capacity', 'the_print']

class Trash(models.Model):
    slug = models.SlugField(blank=True, null=True, max_length=255)
    ref = models.CharField("Référence", max_length=255, blank=True, null=True)
    trash_type = models.CharField("Type de déchet", max_length=250, choices=TYPE_TRASH, null=True, blank=True)
    weight = models.FloatField(null=True, blank=True)
    confirmation_weight = models.FloatField(null=True, blank=True)
    date = models.DateTimeField(null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
    machine = models.ForeignKey('Machine.Machine', on_delete=models.SET_NULL, blank=True, null=True)
    state = models.CharField("Etat", max_length=255, choices=TRASH_STATE, null=True, blank=True)
    whereabouts = models.ForeignKey("Company.Company", on_delete = models.SET_NULL, blank= True, null = True)
    comment = models.CharField("Source", max_length = 255 ,null = True, blank = True)

    def save(self, *args, **kwargs):
        get_ref = self.ref if self.ref is not None else ''
        get_type = self.get_trash_type_display() if self.get_trash_type_display() != None else ""
        get_weight = self.weight if self.weight != None else float(0)
        get_date = self.date if self.date != None else ""
        get_machine = self.machine.__str__() if self.machine.__str__() is not None else 'No_Machine'
        get_user = self.user if self.user is not None else "No_User"

        slug_trash = f"trash-{get_ref}-{get_type}-{get_weight}kg-{get_machine}-{get_user}-{get_date}"
        if self.slug is None:
            self.slug = slugify(slug_trash)
        super(Trash, self).save(*args, **kwargs)

    def __str__(self):
        get_ref = self.ref if self.ref is not None else ''
        get_type = self.get_trash_type_display() if self.get_trash_type_display() != None else ""
        get_weight = self.weight if self.weight != None else float(0)
        get_date = self.date if self.date != None else ""
        get_machine = self.machine.__str__() if self.machine.__str__() is not None else 'No_Machine'
        get_user = self.user if self.user is not None else "No_User"
        return f"Déchet-{get_ref}-{get_type.upper()}-{get_weight} (Kg) {get_machine.upper()}-{get_user}-{get_date}"

    class Meta:
        ordering = ['-date']

class Coil(Product):
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="maker" ,blank=True, null=True)

    printer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="printer" ,blank=True, null=True)
    
    shaper = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="shaper" ,blank=True, null=True)

    introducer = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="introducer", blank=True, null=True)
    capacity = models.CharField("Taille",max_length=255, choices=SIZE, blank=True, null=True)
    the_print = models.CharField("Impression", max_length=250,
                            choices=PRINT_CHOICES, null=True, blank=True)
    micronnage = models.FloatField(
        verbose_name="Micronnage", default=0, blank=True, null=True)

    extrusion_machine = models.ForeignKey('Machine.Machine', blank=True, null = True, on_delete = models.SET_NULL, related_name="extrudeuse")
    printing_machine = models.ForeignKey('Machine.Machine', blank=True, null = True, on_delete = models.SET_NULL, related_name="imprimeuse")
    shaping_machine = models.ForeignKey('Machine.Machine', blank=True, null = True, on_delete = models.SET_NULL, related_name="soudeuse")
    creation_date = models.DateTimeField(null=True, blank=True)
    printing_date = models.DateTimeField(null=True, blank=True)
    shaping_date = models.DateTimeField(null=True, blank=True)
    sale_date = models.DateTimeField(null=True, blank=True)
    supplier = models.ForeignKey(
        "Contact.Contact", verbose_name="Fournisseur", blank=True, null=True, on_delete = models.SET_NULL, related_name = "coil_supplier")
    client = models.ForeignKey(
        "Contact.Contact", verbose_name="Client", blank=True, null=True, on_delete = models.SET_NULL, related_name = "coil_purchaser")
    status = models.CharField(
        max_length=25, blank=True, null=True, default="PENDING_EXTRUSION" ,choices=COIL_STATUS)

    ext_validated = models.BooleanField(blank=True, null=True, default=False)

    motive = models.CharField("Motif", max_length=255 ,blank=True, null=True)
    explanation = models.TextField("Explication" ,blank=True, null=True)
    defective = models.CharField("Bobine Défectueuse", max_length=250,
                            choices=DEFECTIVE_CHOICES, default="NON_DEFECTIVE" , null=True, blank=True)
    printed = models.CharField("Impression", max_length=250,
                            choices=PRINTED , null=True, blank=True)
    cw1 = models.DecimalField(default = 0, null=True, blank=True, decimal_places=3, max_digits=6)
    cw2 = models.DecimalField(default = 0, null=True, blank=True, decimal_places=3, max_digits=6)
    cw3 = models.DecimalField(default = 0, null=True, blank=True, decimal_places=3, max_digits=6)
    cwm = models.DecimalField(default = 0, null=True, blank=True, decimal_places=3, max_digits=6)

    parent = models.ForeignKey("Coil",max_length=200, on_delete= models.SET_NULL,null=True, blank=True)
    is_sub = models.BooleanField("Dérivée", default=False, null=True, blank=True)
    type_coil = models.ForeignKey("CoilType", blank=True, null=True, on_delete=models.SET_NULL)
    destroyed = models.BooleanField("Détruite", default=False, null=True, blank=True)
    quarantine_level = models.IntegerField(blank=True, null=True, default=0)

    ticket_printed = models.BooleanField(blank = True, null = True, default = False)
    
    def save(self, *args, **kwargs):
        get_name = self.name.name if self.name is not None else ''
        get_ref = self.ref if self.ref is not None else ''
        get_print = self.get_the_print_display() if self.the_print != None else ""
        get_capacity = self.get_capacity_display() if self.capacity != None else ""
        get_color = self.color if self.color != None else ""
        get_perfumed = self.get_perfume_display() if self.perfume is not None else ''
        get_flavor = self.flavor if self.flavor is not None else ""

        slug_coil = f"coil-{get_ref}-{get_name}-{get_capacity}l-{get_color}-{get_print}-{get_perfumed}-{get_flavor}"
        if self.cw3 == 0:
            self.cwm = (self.cw1+self.cw2+self.cw3)/2
        elif self.cw2 == 0:
            self.cwm = self.cw1
        elif self.cw3 != 0:
            self.cwm = (self.cw1+self.cw2+self.cw3)/3

        # if self.slug is None:
        self.slug = slugify(slug_coil)
        self.product_designation = self.__str__().upper()
        super(Coil, self).save(*args, **kwargs)

    def get_coil_url(self):
        return reverse("production:update-coil", kwargs={"ref": self.ref})

    def __str__(self):
        get_name = self.name.name if self.name is not None else ''
        get_ref = self.ref if self.ref is not None else ''
        get_print = self.get_the_print_display() if self.the_print != None else ""
        get_capacity = self.get_capacity_display() if self.capacity != None else ""
        get_color = self.color if self.color is not None else ""
        get_perfumed = self.get_perfume_display() if self.perfume == "PERFUMED" else ''
        get_flavor = self.flavor if self.flavor is not None else ""
        if self.flavor is not None:
            return f"{get_ref} {get_name} {get_capacity} {get_color} ({get_print}) [{get_perfumed} {get_flavor}]"
        else:
            return f"{get_ref} {get_name} {get_capacity} {get_color} ({get_print}) {get_perfumed}"

    class Meta:
        ordering = ['-status','-creation_date']


class CoilType(Product):
    capacity = models.CharField("Taille",max_length=255, choices=SIZE, blank=True, null=True)
    the_print = models.CharField("Impression", max_length=250,
                            choices=PRINT_CHOICES, null=True, blank=True)
    micronnage_ideal = models.FloatField(
        verbose_name="Micronnage", default=0, blank=True, null=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    def get_absolute_url(self):
        return reverse("product:coil-update", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        get_name = self.name.name if self.name is not None else ''
        get_print = self.get_the_print_display() if self.the_print != None else ""
        get_capacity = self.get_capacity_display() if self.capacity != None else ""
        get_color = self.color if self.color != None else ""
        get_perfumed = self.get_perfume_display() if self.perfume is not None else ''
        get_flavor = self.flavor if self.flavor is not None else ""
        slug_coiltype = f"coiltype-{get_name}-{get_capacity}l-{get_color}-{get_print}-{get_perfumed}-{get_flavor}"
        # if self.slug is None:
        self.slug = slugify(slug_coiltype)
        self.product_designation = f"Bobine {self.__str__().upper()}"
        super(CoilType, self).save(*args, **kwargs)

    def __str__(self):
        get_name = self.name.name if self.name is not None else ''
        get_print = self.get_the_print_display() if self.the_print != None else ""
        get_capacity = self.get_capacity_display() if self.capacity != None else ""
        get_color = self.color if self.color is not None else ""
        get_perfumed = self.get_perfume_display() if self.perfume == "PERFUMED" else ''
        get_flavor = self.flavor if self.flavor is not None else ""
        if self.flavor is not None:
            return f"{get_name} {get_capacity} {get_color} ({get_print}) [{get_perfumed} {get_flavor}]"
        else:
            return f"{get_name} {get_capacity} {get_color} ({get_print}) {get_perfumed}"

    def quantity_produced(self, start_date, end_date):
        coils = self.coil_set.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date))
        total = 0
        total = coils.count()
        
        return total
    
    def weight_produced(self, start_date, end_date):
        coils = self.coil_set.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date))
        total = 0
        for p in coils:
            total += p.weight
        
        return total

    def quantity_shaped(self, start_date, end_date):
        coils = self.coil_set.filter(Q(shaping_date__lte = end_date) & Q(shaping_date__gte = start_date) & Q(status = "CONSUMED"))
        total = 0
        total = coils.count()
        
        return total
    
    def weight_shaped(self, start_date, end_date):
        coils = self.coil_set.filter(Q(shaping_date__lte = end_date) & Q(shaping_date__gte = start_date) & Q(status = "CONSUMED"))
        total = 0
        for p in coils:
            total += p.weight
        
        return total
        
    def quantity_stock(self):
        coils = self.coil_set.filter(Q(status = "IN_STOCK"))
        total = 0
        total = coils.count()
        
        return total
    
    def weight_stock(self):
        coils = self.coil_set.filter(Q(status = "IN_STOCK"))
        total = 0
        for p in coils:
            total += p.weight
        
        return total

    class Meta:
        ordering = ['name', 'capacity']

class FinishedProduct(Product):
    capacity = models.CharField("Taille",max_length=255, choices=SIZE, blank=True, null=True)
    the_print = models.CharField("Impression", max_length=250,
                            choices=PRINT_CHOICES, null=True, blank=True)
    micronnage = models.FloatField(
        verbose_name="Micronnage", default=0, blank=True, null=True)

    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    creation_date = models.DateTimeField(auto_now_add=True, null=True)
    supplier = models.ManyToManyField(
        "Contact.Contact", verbose_name="Fournisseur", blank=True)

    def save(self, *args, **kwargs):
        get_name = self.name.name if self.name is not None else ''
        get_print = self.get_the_print_display() if self.the_print != None else ""
        get_capacity = self.get_capacity_display() if self.capacity != None else ""
        get_color = self.color if self.color != None else ""
        get_perfumed = self.perfume if self.perfume is not None else ''

        slug_finished_product = f"finishedproduct-{get_name}-{get_capacity}l-{get_color}-{get_print}-{get_perfumed}"
        if self.slug is None:
            self.slug = slugify(slug_finished_product)
        super(FinishedProduct, self).save(*args, **kwargs)

    def get_final_product_url(self):
        return reverse("product:final-product-update", kwargs={"slug": self.slug})

    def __str__(self):
        get_name = self.name.name if self.name is not None else ''
        get_print = self.get_the_print_display() if self.the_print != None else ""
        get_capacity = self.get_capacity_display() if self.capacity != None else ""
        get_color = self.color if self.color != None else ""
        get_perfumed = self.perfume if self.perfume is not None and self.perfume == "PERFUMED" else ''
        return f"{get_name} {get_capacity} {get_color} ({get_print}) {get_perfumed}"

class FinishedProductType(Product):
    capacity = models.CharField("Taille",max_length=255, choices=SIZE, blank=True, null=True)
    the_print = models.CharField("Impression", max_length=250,
                            choices=PRINT_CHOICES, null=True, blank=True)
    micronnage = models.FloatField(
        verbose_name="Micronnage", default=0, blank=True, null=True)
    bag_roll = models.PositiveIntegerField(
        "Nombre de sacs par rouleau", default=0, blank=True, null=True)
    roll_package = models.PositiveIntegerField(
        "Nombre de rouleaux par carton", default=0, blank=True, null=True)
    package = models.ForeignKey("Package", on_delete=models.SET_NULL ,null=True, blank=True)
    labelling = models.ForeignKey("Labelling", on_delete=models.SET_NULL ,null=True, blank=True)

    def get_absolute_url(self):
        return reverse("product:final-product-update", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        get_name = self.name.name if self.name is not None else ''
        get_print = self.get_the_print_display() if self.the_print != None else ""
        get_capacity = self.get_capacity_display() if self.capacity != None else ""
        get_color = self.color if self.color != None else ""
        get_perfumed = self.perfume if self.perfume is not None else ''
        get_flavor = self.flavor if self.flavor is not None else ""
        get_bag_roll = self.bag_roll if self.bag_roll is not None else int(0)
        get_roll_package = self.roll_package if self.roll_package is not None else int(0)
        slug_finishedproducttype = f"finishedproducttype-{get_name}-{get_capacity}l-{get_color}-{get_print}-{get_perfumed}-{get_flavor}-{get_bag_roll}x{get_roll_package}"
        # if self.slug is None:
        self.slug = slugify(slug_finishedproducttype)
        self.product_designation = f"Produit Fini {self.__str__().upper()}"
        super(FinishedProductType, self).save(*args, **kwargs)

    def __str__(self):
        get_name = self.name.name if self.name is not None else ''
        get_print = self.get_the_print_display() if self.the_print != None else ""
        get_capacity = self.get_capacity_display() if self.capacity != None else ""
        if self.color is not None and self.color.name !="autre":
            get_color = self.color
        else:
            get_color=""
        get_perfumed = self.get_perfume_display() if self.perfume == "PERFUMED" else ''
        get_flavor = self.flavor if self.flavor is not None else ""
        get_bag_roll = self.bag_roll if self.bag_roll is not None else int(0)
        get_roll_package = self.roll_package if self.roll_package is not None else int(0)
        if self.flavor is not None:
            return f"{get_name} {get_capacity} {get_color} ({get_print}) [{get_bag_roll}x{get_roll_package}] [{get_perfumed} {get_flavor}]"
        else:
            return f"{get_name} {get_capacity} {get_color} ({get_print}) [{get_bag_roll}x{get_roll_package}] {get_perfumed}"

    def quantity_produced(self, start_date, end_date):
        productions = self.ProduitCible.filter(Q(date__lte = end_date) & Q(date__gte = start_date))
        total = 0
        for p in productions:
            if p.quantity_produced is not None:
                total += p.quantity_produced
        
        return total
    
    def user_quantity_produced(self, start_date, end_date, user):
        productions = self.ProduitCible.filter(Q(user = user) & Q(date__lte = end_date) & Q(date__gte = start_date))
        total = 0
        for p in productions:
            if p.quantity_produced is not None:
                total += p.quantity_produced
        
        return total

    def quantity_sold(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) & Q(type_order = "STOCK_OUT"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item.product_designation == self.product_designation:
                    total += i.quantity
        
        return total

    class Meta:
        ordering = ['name', 'capacity']
        
class RawMatter(Product):
    supplier = models.ManyToManyField(
        "Contact.Contact", verbose_name="Fournisseur", blank=True)

    def get_absolute_url(self):
        return reverse("product:raw-matter-update", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        get_name = self.name.name if self.name is not None else ''
        get_type = self.get_type_name_display() if self.get_type_name_display() != None and self.type_name != "AUTRE" else ""
        get_weight = self.weight if self.weight != None else int(0)
        get_color = self.color if self.color != None and self.color.name != 'autre' else ""
        get_perfumed = self.perfume if self.perfume is not None else ''
        get_flavor = self.flavor if self.flavor is not None else ""
        get_brand = self.brand if self.brand is not None else ''
        slug_rawmatter = f"rawmatter-{get_brand}-{get_name}-{get_type}-{get_perfumed}-{get_flavor}-{get_color}-{get_weight}Kg-{self.id}"
        if self.slug is None:
            self.slug = slugify(slug_rawmatter)
        self.product_designation = ' '.join(self.__str__().split()).upper()
        super(RawMatter, self).save(*args, **kwargs)

    def __str__(self):
        get_name = self.name.name if self.name is not None else ''
        get_type = self.get_type_name_display() if self.get_type_name_display() is not None and self.type_name != "AUTRE" else ""
        get_weight = self.weight if self.weight != None else int(0)
        get_color = self.color if self.color != None and self.color.name != 'autre' else ""
        get_perfumed = self.get_perfume_display() if self.perfume == 'PERFUMED' else ''
        get_flavor = self.flavor if self.flavor is not None else ""
        if self.flavor is not None:
            return f"[{self.brand.name}] {get_name} {get_type} {get_perfumed} {get_flavor} {get_color} {get_weight} Kg"
        else:
            return f"[{self.brand.name}] {get_name} {get_type} {get_perfumed} {get_color} {get_weight} Kg"

    
    def quantity_consumed(self, start_date, end_date):
        orders = Order.objects.exclude(machine = None).filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item.product_designation == self.product_designation:
                    total += i.quantity
        
        return total
    
    def quantity_brought(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) &  Q(type_order = "STOCK_ENTRY") & Q(category = "Matière Première"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item.product_designation == self.product_designation:
                    total += i.quantity
        
        return total
    
    def our_quantity_brought(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) &  Q(type_order = "STOCK_ENTRY") & Q(category = "Matière Première") & Q(supplier__first_name = "PLAST") & Q(supplier__last_name = "LN"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item.product_designation == self.product_designation:
                    total += i.quantity
        
        return total
    
    def our_quantity_taken(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) &  Q(type_order = "STOCK_OUT") & Q(category = "Matière Première") & Q(company__name = "Ln Plast"))
        total = 0
        for o in orders:
            for i in o.items.all():
                if i.item.product_designation == self.product_designation:
                    total += i.quantity
        
        return total
        
    
    class Meta:
        ordering = ['name','type_name', '-brand']

class Handle(models.Model):
    slug = models.SlugField(unique=False, blank=True,
                            null=True, max_length=255)    
    brand = models.ForeignKey(
        "Brand", on_delete=models.CASCADE,related_name="handle_brand" ,verbose_name="Marque", blank=True, null=True)
    color = models.ForeignKey(
        "Color", on_delete=models.CASCADE,related_name="handle_color" ,verbose_name="Couleur", blank=True, null=True)
    quantity = models.PositiveIntegerField(
        "Quantité", default=0, blank=True, null=True, validators=[MinValueValidator(0)])
    threshold = models.PositiveIntegerField(
        "Seuil", default=0, blank=True, null=True)
    quantity_workshop = models.PositiveIntegerField(
        "Quantité dans l'atelier", default=0, blank=True, null=True, validators=[MinValueValidator(0)])
    designation = models.CharField(max_length=255, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse("product:handle-update", kwargs={"slug": self.slug})
    def get_delete_url(self):
        return reverse("product:handle-delete", kwargs={"slug": self.slug})
    def get_add_to_order_url(self):
        return reverse("stock-manager:add-to-order", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        get_color = self.color.name if self.color != None and self.color.name != 'autre' else ""
        get_brand = self.brand.name if self.brand is not None else ""
        slug_handle = f"handle-{get_brand}-{get_color}"
        self.designation = self.__str__()
        if self.slug is None:
            self.slug = slugify(slug_handle)
        super(Handle, self).save(*args, **kwargs)

    def __str__(self):
        get_color = self.color.name if self.color != None and self.color.name != 'autre' else ""
        get_brand = self.brand.name if self.brand is not None else ""
        return f"Cordon [{get_brand}] {get_color}"

    def quantity_consumed(self, start_date, end_date):
        consumptions = self.handle_consumed.filter(Q(date__lte = end_date) & Q(date__gte = start_date))
        total = 0
        for p in consumptions:
            if p.quantity is not None:
                total += p.quantity
        
        return total
    
    def quantity_brought(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) &  Q(type_order = "STOCK_ENTRY") & Q(category = "Cordon"))
        total = 0
        for o in orders:
            for i in o.handles.all():
                if i.item == self:
                    total += i.quantity
        
        return total

    class Meta:
        ordering = ['brand', '-color']

class Labelling(models.Model):
    slug = models.SlugField(unique=False, blank=True,
                            null=True, max_length=255)    
    name = models.ForeignKey(Range, on_delete=models.SET_NULL, blank=True, null=True)
    capacity = models.CharField(
        "Taille",max_length=255,choices=SIZE, blank=True, null=True)
    the_print = models.CharField("Impression", max_length=250,
                            choices=PRINT_CHOICES, null=True, blank=True)
    perfume = models.CharField(max_length=250, blank=True, null=True, choices=PERFUMED)
    quantity = models.PositiveIntegerField(
        "Quantité", default=0, blank=True, null=True, validators=[MinValueValidator(0)])
    threshold = models.PositiveIntegerField(
        "Seuil", default=0, blank=True, null=True)
    quantity_workshop = models.PositiveIntegerField(
        "Quantité dans l'atelier", default=0, blank=True, null=True, validators=[MinValueValidator(0)])
    designation = models.CharField(max_length=255, blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse("product:labelling-update", kwargs={"slug": self.slug})
    def get_delete_url(self):
        return reverse("product:labelling-delete", kwargs={"slug": self.slug})
    def get_add_to_order_url(self):
        return reverse("stock-manager:add-to-order", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        get_range = self.name.name if self.name is not None else ""
        get_capacity = self.get_capacity_display() if self.capacity is not None else ""
        get_print = self.get_the_print_display() if self.the_print is not None else ""
        get_perfume = self.get_perfume_display() if self.perfume is not None else ""
        slug_labelling = f"labelling-{get_range}-{get_capacity}-l-{get_print}-{get_perfume}"
        self.designation = self.__str__()
        if self.slug is None:
            self.slug = slugify(slug_labelling)
        super(Labelling, self).save(*args, **kwargs)

    def __str__(self):
        get_range = self.name.name if self.name is not None else ""
        get_capacity = self.get_capacity_display() if self.capacity is not None else ""
        get_print = self.get_the_print_display() if self.the_print is not None else ""
        get_perfume = self.get_perfume_display() if self.perfume is not None else ""
        return f"Labelling {get_range} {get_capacity} ({get_print}) {get_perfume}"

    def quantity_consumed(self, start_date, end_date):
        consumptions = self.labelling_consumed.filter(Q(date__lte = end_date) & Q(date__gte = start_date))
        total = 0
        for p in consumptions:
            if p.quantity is not None:
                total += p.quantity
        
        return total
    
    def quantity_brought(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) &  Q(type_order = "STOCK_ENTRY") & Q(category = "Labelling"))
        total = 0
        for o in orders:
            for i in o.labellings.all():
                if i.item == self:
                    total += i.quantity
        
        return total

    class Meta:
        ordering = ['name','capacity']

class Package(models.Model):
    slug = models.SlugField(unique=False, blank=True,
                            null=True, max_length=255)    
    name = models.ForeignKey(Range, on_delete=models.SET_NULL, blank=True, null=True)
    capacity = models.CharField("Taille",max_length=255, choices=SIZE, blank=True, null=True)
    the_print = models.CharField("Impression", max_length=250,
                            choices=PRINT_CHOICES, null=True, blank=True)
    perfume = models.CharField(max_length=250, blank=True, null=True, choices=PERFUMED)
    quantity = models.PositiveIntegerField(
        "Quantité", default=0, blank=True, null=True, validators=[MinValueValidator(0)])
    threshold = models.PositiveIntegerField(
        "Seuil", default=0, blank=True, null=True)
    quantity_workshop = models.PositiveIntegerField(
        "Quantité dans l'atelier", default=0, blank=True, null=True, validators=[MinValueValidator(0)])
    designation = models.CharField(max_length=255, blank=True, null=True)
    def get_absolute_url(self):
        return reverse("product:package-update", kwargs={"slug": self.slug})
    def get_delete_url(self):
        return reverse("product:package-delete", kwargs={"slug": self.slug})
    def get_add_to_order_url(self):
        return reverse("stock-manager:add-to-order", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        get_range = self.name.name if self.name is not None else ""
        get_capacity = self.get_capacity_display() if self.capacity is not None else ""
        get_print = self.get_the_print_display() if self.the_print is not None else ""
        get_perfume = self.get_perfume_display() if self.perfume is not None else ""
        slug_package = f"package-{get_range}-{get_capacity}-l-{get_print}-{get_perfume}"
        self.designation = self.__str__()
        if self.slug is None:
            self.slug = slugify(slug_package)
        super(Package, self).save(*args, **kwargs)

    def __str__(self):
        get_range = self.name.name if self.name is not None else ""
        get_capacity = self.get_capacity_display() if self.capacity is not None else ""
        get_print = self.get_the_print_display() if self.the_print is not None else ""
        get_perfume = self.get_perfume_display() if self.perfume is not None else ""    
        return f"EMBALLAGE {get_range.upper()} {get_capacity} {get_print.upper()} {get_perfume.upper()}"
    
    def quantity_consumed(self, start_date, end_date):
        consumptions = self.package_consumed.filter(Q(date__lte = end_date) & Q(date__gte = start_date))
        total = 0
        for p in consumptions:
            if p.quantity is not None:
                total += p.quantity
        
        return total
    
    def quantity_brought(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) &  Q(type_order = "STOCK_ENTRY") & Q(category = "Emballage"))
        total = 0
        for o in orders:
            for i in o.packages.all():
                if i.item == self:
                    total += i.quantity
        
        return total
    
    class Meta:
        ordering = ['name','capacity']


class Tape(models.Model):
    slug = models.SlugField(unique=False, blank=True,
                            null=True, max_length=255)    
    brand = models.ForeignKey(
        "Brand", on_delete=models.CASCADE,related_name="tape_brand" ,verbose_name="Marque", blank=True, null=True)
    quantity = models.PositiveIntegerField(
        "Quantité", default=0, blank=True, null=True, validators=[MinValueValidator(0)])
    threshold = models.PositiveIntegerField(
        "Seuil", default=0, blank=True, null=True)
    quantity_workshop = models.PositiveIntegerField(
        "Quantité dans l'atelier", default=0, blank=True, null=True, validators=[MinValueValidator(0)])
    tape_type = models.CharField("Type",max_length=255, default=0, blank=True, null=True, choices =TAPE_TYPE )
    
    def get_absolute_url(self):
        return reverse("product:tape-update", kwargs={"slug": self.slug})
    def get_delete_url(self):
        return reverse("product:tape-delete", kwargs={"slug": self.slug})
    def get_add_to_order_url(self):
        return reverse("stock-manager:add-to-order", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        get_brand = self.brand.name if self.brand is not None else ""
        get_type = self.get_tape_type_display() if self.tape_type is not None else ""
        slug_tape = f"tape-{get_brand}-{get_type}"
        if self.slug is None:
            self.slug = slugify(slug_tape)
        super(Tape, self).save(*args, **kwargs)

    def __str__(self):
        get_brand = self.brand.name if self.brand is not None else ""
        get_type = self.get_tape_type_display() if self.tape_type is not None else ""
        return f"Scotch [{get_brand}] {get_type}"

class SparePart(models.Model):
    slug = models.SlugField(unique=False, blank=True,
                            null=True, max_length=255)
    name = models.CharField("Désignation ENG",null=True, blank=True, max_length=200)
    name_fr = models.CharField("Désignation FR",null=True, blank=True, max_length=200)
    ref = models.CharField("Référence",null=True, blank=True, max_length=200, unique=True)
    quantity = models.PositiveIntegerField(
        "Quantité", default=0, blank=True, null=True, validators=[MinValueValidator(0)])
    threshold = models.PositiveIntegerField(
        "Seuil", default=0, blank=True, null=True)
    price = models.FloatField('Prix', null=True, blank=True)
    category = models.CharField("Catégorie",null=True, blank=True, max_length=200, choices=TYPE_PIECE)
    

    def quantity_consumed(self, start_date, end_date):
        consumptions = SparePartConsumption.objects.filter(Q(date__lte = end_date) & Q(date__gte = start_date))
        total = 0
        for c in consumptions:
            if c.part.slug == self.slug:
                total += c.quantity
        
        return total

    def quantity_brought(self, start_date, end_date):
        orders = Order.objects.filter(Q(ordered_date__lte = end_date) & Q(ordered_date__gte = start_date) &  Q(type_order = "STOCK_ENTRY") & Q(category = "Pièce de Rechange"))
        total = 0
        for o in orders:
            for i in o.parts.all():
                if i.item == self:
                    total += i.quantity
        
        return total
        
    def get_absolute_url(self):
        return reverse("product:part-update", kwargs={"ref": self.ref})
    def get_delete_url(self):
        return reverse("product:part-delete", kwargs={"ref": self.ref})
    def get_add_to_order_url(self):
        return reverse("stock-manager:add-to-order", kwargs={"slug": self.slug})
    def save(self, *args, **kwargs):
        get_name = self.name if self.name is not None else ""
        get_ref = self.ref if self.ref is not None else ""
        get_category = self.get_category_display() if self.category is not None else ""
        slug_part = f"part-{get_name}-{get_ref}-{get_category}"
        if self.slug is None:
            self.slug = slugify(slug_part)
        super(SparePart, self).save(*args, **kwargs)

    def __str__(self):
        get_name = self.name if self.name is not None else ""
        get_ref = self.ref if self.ref is not None else ""
        return f"[{get_ref}] {get_name}"