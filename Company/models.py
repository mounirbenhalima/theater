from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=200,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    fax = models.CharField(max_length=50,blank=True,null=True)
    mobile = models.CharField(max_length=50,blank=True,null=True)
    address = models.CharField(max_length=255, null=True,blank=True)
    logo = models.ImageField(null=True,blank=True)

    
    def __str__(self):
        return self.name