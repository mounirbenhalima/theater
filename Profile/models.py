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
    hiring_date = models.DateField(blank=True, null = True)
    job_position = models.ForeignKey('JobPosition', on_delete=models.SET_NULL ,verbose_name="Postes",null=True,blank=True)
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

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
        db_table = 'Profile'