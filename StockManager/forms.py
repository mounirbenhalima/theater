from django import forms
from django.db.models import Q
from .models import Order, OrderItem, SparePartConsumption
from Contact.models import Contact
from .choices import CONSUMPTION_TYPE, INTERVENTION_TYPE
from StockManager.models import TrashOut, CoilSale
from Product.choices import TYPE_TRASH
from Product.models import Coil, CoilType, SparePart
from Machine.models import Machine
from Company.models import Company
from django.contrib.auth.models import User

class ContactChoiceForm(forms.ModelForm):

    supplier = forms.ModelChoiceField(
        required=False,
        queryset=Contact.objects.filter(contact_type = "SUPPLIER") | Contact.objects.filter(contact_type = "WORKSHOP"),
        label="Client/Fournisseur",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-sm",
            }
        ))
    intern_user = forms.ModelChoiceField(
        required=False,
        queryset=User.objects.filter(profile__job_position__name ="Mélangeur") | User.objects.filter(profile__job_position__name ="Opérateur Impression"),
        label="Opérateur",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-sm",
            }
        ))
    company = forms.ModelChoiceField(
        required=False,
        queryset=Company.objects.all(),
        label="Destination",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-sm",
            }
        ))
    
    client = forms.ModelChoiceField(
        required=False,
        queryset=Contact.objects.filter(contact_type = "CLIENT"),
        label="Client",
        widget=forms.Select(
            attrs={
                "class": "form-control form-control-sm",
            }
        )
    )
    
    type_consumption = forms.CharField(
        required=False,
        label="Type du Sortie",
        widget=forms.Select(
            choices=CONSUMPTION_TYPE,
            attrs={
                "class": "form-control form-control-sm",
            }
        ))

    machine = forms.ModelChoiceField(
        required=False,
        queryset=Machine.objects.filter(machine_type__name='Mélangeur', state = "FREE"),
        widget=forms.Select(
            attrs={
                "class": "form-control"
            }
        ))
    

    class Meta:
        model = Order
        fields = ["supplier", "type_consumption", "client", "intern_user", "company", "machine"]

class TrashOutForm(forms.ModelForm):
    class Meta:
        model = TrashOut
        fields = ['trash_type', 'destination', 'weight']

    trash_type = forms.CharField(label="Type Déchet",
                           widget=forms.Select(
                               choices=TYPE_TRASH,
                               attrs={
                                   "class": "form-control",
                               }
                           ))

    weight = forms.FloatField(label="Poids Déchet",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          "step":"0.01",
                                          'min'  : "0"
                                      }
                                  )) 
    
    destination = forms.ModelChoiceField(
        label="Destination",
        queryset=Company.objects.exclude(name="Ln Plast").all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))

class CoilEntryForm(forms.ModelForm):
    class Meta:
        model = Coil
        fields = ['type_coil', 'supplier']

    type_coil = forms.ModelChoiceField(
        label="Bobine Produite",
        queryset=CoilType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
        
        )
    supplier = forms.ModelChoiceField(
        label="Provenance",
        queryset=Contact.objects.filter(contact_type = "SUPPLIER"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
        
        )
    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class SparePartConsumptionForm(forms.ModelForm):
    class Meta:
        model = SparePartConsumption
        fields = ['part', 'machine', 'quantity', 'intervention_type']

    part = forms.ModelChoiceField(label="Pièce",
                            queryset=SparePart.objects.filter(quantity__gt=0),
                            widget=forms.Select(   
                               attrs={
                                   "class": "form-control",
                               }
                           ))

    machine = forms.ModelChoiceField(
        label="Machine",
        queryset=Machine.objects.filter(Q(machine_type__name="Soudeuse")),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    quantity = forms.IntegerField(label="Nombre d'Unités",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  )) 
    intervention_type = forms.CharField(label="Type Maintenance",
                           widget=forms.Select(
                               choices=INTERVENTION_TYPE,
                               attrs={
                                   "class": "form-control",
                               }
                           ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class CoilSaleForm(forms.ModelForm):
    class Meta:
        model = CoilSale
        fields = ['client']

    client = forms.ModelChoiceField(
        label="Client",
        queryset=Contact.objects.filter(contact_type = "CLIENT"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data