from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
from django.db.models import Q


def get_user_name(self):
    get_job_position = self.profile.job_position.name if self.profile.job_position is not None else ""
    get_first_name = self.first_name if self.first_name is not None else "Anonyme"
    get_last_name = self.last_name if self.last_name is not None else "Anonyme"
    return f'{get_job_position}: {get_first_name} {get_last_name}'

User.add_to_class("__str__", get_user_name)


HOLIDAY_REQUEST = (
    ('PENDING','En Attente'),
    ('ACCEPTED','Validé'),
    ('REJECTED','Rejeté'),
)

HOLIDAY_MOTIVES = (
    ('ANNUAL','Congé Annuel'),
    ('MARRIAGE','Mariage'),
    ('BIRTH','Naissance'),
    ('HEALTH','Problème de Santé'),
    ('OTHER','Autre'),
)


class JobPosition(models.Model):
    name = models.CharField(
                'Intitulé du poste',
                max_length=200,
                unique=True,
                blank=True,
                null=True
                )
    slug = models.SlugField(unique = False, blank = True, null= True)
    # def get_absolute_url(self):
    #     return reverse("profile-update", kwargs={"slug": self.slug})

    def get_absolute_url(self):
        return reverse("jobposition-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("jobposition-delete", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Poste'
        verbose_name_plural = 'Postes'
        db_table = 'JobPosition'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not JobPosition.objects.filter(slug=self.slug).exists():
            _slug = f"{self.name}"
            self.slug = slugify(_slug)

        super(JobPosition, self).save(*args, **kwargs)


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True, verbose_name='Utilisateur')
    slug = models.SlugField(unique = False, blank = True, null= True)
    group = models.IntegerField(blank=True, null = True)

    hiring_date = models.DateField(blank=True, null = True)

    bonus = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=5)

    image = models.ImageField(blank=True,null=True, verbose_name="Image")
    birth_day = models.DateField("Date de Naissance",blank=True, null=True)
    mobile = models.CharField(max_length=20,null=True,blank=True)
    address = models.CharField(max_length=255,null=True,blank=True)
    job_position = models.ForeignKey('JobPosition', on_delete=models.SET_NULL ,verbose_name="Postes",null=True,blank=True)
    company = models.ForeignKey('Company.Company',on_delete=models.SET_NULL,null=True,blank=True)
    city = models.CharField(max_length=255,blank=True,null=True)
    rest_holiday = models.PositiveIntegerField(blank = True, null= True, default=0)
    salary = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=10)
    self_transported = models.BooleanField(null=True, blank=True, default = False)
    active = models.BooleanField(null=True, blank=True, default = True)

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    def get_absolute_url(self):
        return reverse("profile-update", kwargs={"slug": self.slug})

    def get_delete_url(self):
        return reverse("profile-delete", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        if not Profile.objects.filter(slug=self.slug).exists():
            _slug = f"{self.user.id} {self.user.first_name} {self.user.last_name}"
            self.slug = slugify(_slug)

        super(Profile, self).save(*args, **kwargs)

    def extrusion_number(self, start_date, end_date):
        coils = self.user.maker.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date))
        total = coils.count()
        
        return total

    def extrusion_weight(self, start_date, end_date):
        coils = self.user.maker.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date))
        total = 0
        for c in coils:
            total += c.weight
        
        return total

    def printing_number(self, start_date, end_date):
        coils = self.user.printer.exclude(status = "CUT").filter(Q(printing_date__lte = end_date) & Q(printing_date__gte = start_date))
        total = coils.count()
        
        return total

    def printing_weight(self, start_date, end_date):
        coils = self.user.printer.exclude(status = "CUT").filter(Q(printing_date__lte = end_date) & Q(printing_date__gte = start_date))
        total = 0
        for c in coils:
            total += c.weight
        
        return total

    def shaping_number(self, start_date, end_date):
        coils = self.user.shaper.exclude(status = "CUT").filter(Q(shaping_date__lte = end_date) & Q(shaping_date__gte = start_date))
        total = coils.count()
        
        return total

    def shaping_weight(self, start_date, end_date):
        coils = self.user.shaper.exclude(status = "CUT").filter(Q(shaping_date__lte = end_date) & Q(shaping_date__gte = start_date))
        total = 0
        for c in coils:
            total += c.weight
        
        return total

    def production_number(self, start_date, end_date):
        productions = self.user.production_set.filter(Q(date__lte = end_date) & Q(date__gte = start_date) & Q(process_type = "FINISHED_PRODUCT"))
        total = 0
        for i in productions:
            total += i.quantity_produced

        return total

    def production_weight(self, start_date, end_date):
        productions = self.user.production_set.filter(Q(date__lte = end_date) & Q(date__gte = start_date) & Q(process_type = "FINISHED_PRODUCT"))
        total = 0
        for i in productions:
            total += i.quantity_produced * i.product.weight
            
        return total
        

    def trash_weight(self, start_date, end_date):
        trash = self.user.trash_set.filter(Q(date__lte = end_date) & Q(date__gte = start_date))
        total = 0
        for t in trash:
            total += t.weight
        
        return total


    def defective_number(self, start_date, end_date):
        coils = self.user.maker.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(defective = "DEFECTIVE"))
        total = coils.count()
        
        return total

    def defective_weight(self, start_date, end_date):
        coils = self.user.maker.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(defective = "DEFECTIVE"))
        total = 0
        for c in coils:
            total += c.weight
        
        return total

    def quarantine_number(self, start_date, end_date):
        coils = self.user.maker.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(status = "QUARANTINE"))
        total = coils.count()
        
        return total

    def quarantine_weight(self, start_date, end_date):
        coils = self.user.maker.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(status = "QUARANTINE"))
        total = 0
        for c in coils:
            total += c.weight
        
        return total

    def destroy_number(self, start_date, end_date):
        coils = self.user.maker.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(status = "TO_BE_DESTROYED"))
        total = coils.count()
        
        return total

    def destroy_weight(self, start_date, end_date):
        coils = self.user.maker.exclude(status = "CUT").filter(Q(creation_date__lte = end_date) & Q(creation_date__gte = start_date) & Q(status = "TO_BE_DESTROYED"))
        total = 0
        for c in coils:
            total += c.weight
        
        return total

    def presence_time(self, start_date, end_date):
        points = Point.objects.filter(Q(start_date__lte = end_date) & Q(start_date__gte = start_date) & Q(user = self.user))
        total_m = 0
        total_h = 0
        for p in points:
            total_h += p.hours
            total_m += p.minutes
        
        total_h += total_m // 60
        total_m = total_m % 60
        
        total = f'{total_h}h{total_m}m'
        return total
    
    def absence_time(self, start_date, end_date):
        points = Point.objects.filter(Q(start_date__lte = end_date) & Q(start_date__gte = start_date) & Q(user = self.user))
        total = 0
        for p in points:
            total += p.absence
        
        return total

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'Profile'
        ordering = ['group']


class HolidayRequest(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, related_name = "holiday_requester", verbose_name='Utilisateur')
    validator = models.ForeignKey(User,on_delete=models.SET_NULL,null=True,related_name = "holiday_validator", verbose_name='Utilisateur')
    slug = models.SlugField(max_length = 255, unique = False, blank = True, null= True)

    request_date = models.DateTimeField(null = True)
    start_date = models.DateField()
    end_date = models.DateField()
    validation_date = models.DateTimeField(null = True)

    duration = models.IntegerField(null=True, blank=True)
    address = models.CharField("Adresse", max_length=255, null=True, blank=True)
    mobile = models.CharField(max_length=20,null=True,blank=True)

    motive = models.CharField(max_length=255, null=True, blank=True, choices=HOLIDAY_MOTIVES)

    state = models.CharField(blank=True, null=True, max_length=255, choices = HOLIDAY_REQUEST)

    substitute = models.ForeignKey(User, blank=True, null= True, on_delete=models.SET_NULL, related_name="substitute_holiday")


    def __str__(self):
        return f'Congé {self.user.first_name} {self.user.last_name} {self.start_date} {self.end_date}'

    def save(self, *args, **kwargs):
        if not HolidayRequest.objects.filter(slug=self.slug).exists():
            _slug = f"holiday-{self.user}{self.start_date}{self.end_date}"
            self.slug = slugify(_slug)

        super(HolidayRequest, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Congé'
        verbose_name_plural = 'Congés'
        db_table = 'Holiday'
        ordering = ['-state','request_date']

class Point(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, verbose_name='Utilisateur')
    slug = models.SlugField(unique = False, blank = True, null= True, max_length=255)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    
    duration = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=5)
    hours = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=5)
    minutes = models.DecimalField(null=True, blank=True, decimal_places=0, max_digits=5)

    quality = models.DecimalField(null=True, blank=True, default = 0, decimal_places=1, max_digits=5)
    quantity = models.DecimalField(null=True, blank=True, default = 0, decimal_places=1, max_digits=5)
    motivation = models.DecimalField(null=True, blank=True, default = 0, decimal_places=1, max_digits=5)
    attitude = models.DecimalField(null=True, blank=True, default = 0, decimal_places=1, max_digits=5)
    punctuality = models.DecimalField(null=True, blank=True, default = 0, decimal_places=1, max_digits=5)
    look = models.DecimalField(null=True, blank=True, default = 0, decimal_places=1, max_digits=5)
    penality = models.DecimalField(null=True, blank=True, default = 0, decimal_places=1, max_digits=5)
    prime = models.DecimalField(null=True, blank=True, default = 0, decimal_places=1, max_digits=5)

    absence  = models.DecimalField(null=True, blank=True, decimal_places=1, max_digits=5)

    holiday  = models.BooleanField(null=True, blank=True)    
    is_absent = models.BooleanField(null=True, blank=True)
    valid = models.BooleanField(null=True, blank=True)

    def __str__(self):
        return f'Pointage {self.user.first_name} {self.user.last_name} {self.start_date} {self.end_date}'

    def save(self, *args, **kwargs):
        if not Point.objects.filter(slug=self.slug).exists():
            _slug = f"pointage-{self.id}{self.user}{self.start_date}{self.end_date}"
            self.slug = slugify(_slug)

        super(Point, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Pointage'
        verbose_name_plural = 'Pointages'
        db_table = 'Point'
        ordering = ['user','start_date']

class Salary(models.Model):
    date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null=True, verbose_name='Utilisateur')
    slug = models.SlugField(unique = False, blank = True, null= True, max_length=255)

    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)

    base_salary = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    salary = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    bonus = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    iep = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    irg = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    panier = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    ss = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    trans = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    net = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    cotisable = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    imposable = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    holiday = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=0)
    valid = models.BooleanField(blank=True, null=True)

    def __str__(self):
        return f'Salaire {self.user.first_name} {self.user.last_name} {self.start_date} {self.end_date}'

    def save(self, *args, **kwargs):
        if not Salary.objects.filter(slug=self.slug).exists():
            _slug = f"salaire-{self.date}{self.user}{self.start_date}{self.end_date}{self.salary}"
            self.slug = slugify(_slug)

        super(Salary, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Salary'
        verbose_name_plural = 'Salaries'
        db_table = 'Salary'
        ordering = ['valid','-date']