from django import forms
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Production
from StockManager.models import Warehouse
from Contact.models import Contact

from Product.choices import PRINT_CHOICES, TYPE_PRODUCT, TYPE_PIECE, TYPE_TRASH, PRINTED, COIL_STATUS, PERFUMED
from Machine.models import Machine, MachineStop
from Machine.choices import MACHINE_STOP
from .models import Production, HandleConsumption, LabellingConsumption, InkConsumption
from Product.models import (
    Brand,
    Color,
    Range,
    Product,
    FinishedProductType,
    CoilType,
    Coil,
    FinishedProduct,
    Trash,
    Handle,
    Labelling,
    RawMatter,
    Flavor
)


class ExtrusionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['coil_type', 'machine']

    coil_type = forms.ModelChoiceField(
        label="Bobine Produite",
        queryset=CoilType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
        
        )

    machine = forms.ModelChoiceField(
        label="Extrudeuse",
        queryset=Machine.objects.filter(Q(machine_type__name="Extrudeuse", state = "FREE")),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    

class CoilForm(forms.ModelForm):
    class Meta:
        model = Coil
        fields = [
        "name",
        "capacity",
        "color",
        "the_print",
        "extrusion_machine",
        "printing_machine",
        "shaping_machine",
        "weight",
        "micronnage",
        "cw1",
        "cw2",
        "cw3",
        "type_coil",
        "printed",
        "perfume",
        "flavor",
        # "status"
        ]
    
    name = forms.ModelChoiceField(
        label="Gamme",
        queryset=Range.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    capacity = forms.IntegerField(label="Capacité",
                              required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      "class": "form-control",
                                      "type": "number",
                                  }
                              ))

    color = forms.ModelChoiceField(
        label="Couleur",
        queryset=Color.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    the_print = forms.CharField(label="Lien",
                           widget=forms.Select(
                               choices=PRINT_CHOICES,
                               attrs={
                                   "class": "form-control",
                               }
                           ))
    extrusion_machine = forms.ModelChoiceField(
        required=False,
        label="Extrudeuse",
        queryset=Machine.objects.filter(machine_type__name = "Extrudeuse"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    # 
    printing_machine = forms.ModelChoiceField(
        required=False,
        label="Imprimeuse",
        queryset=Machine.objects.filter(machine_type__name = "Imprimeuse"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    # 
    shaping_machine = forms.ModelChoiceField(
        required=False,
        label="Soudeuse",
        queryset=Machine.objects.filter(machine_type__name = "Soudeuse"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))

    weight = forms.DecimalField(label="Poids",
                              widget=forms.TextInput(
                                  attrs={
                                      "class": "form-control",
                                      "type": "number",
                                      "step":"0.1",
                                  }
                              ))
    micronnage = forms.FloatField(label="Micronnage",
                              widget=forms.TextInput(
                                  attrs={
                                      "class": "form-control",
                                      "type": "number",
                                  }
                              ))
    cw1 = forms.DecimalField(label="Poids Contôle 1",
                              required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      "class": "form-control",
                                      "type": "number",
                                      "step":"0.001",
                                  }
                              ))
    cw2 = forms.DecimalField(label="Poids Contôle 2",
                              required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      "class": "form-control",
                                      "type": "number",
                                      "step":"0.001",
                                  }
                              ))
    cw3 = forms.DecimalField(label="Poids Contôle 3",
                              required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      "class": "form-control",
                                      "type": "number",
                                      "step":"0.001",
                                  }
                              ))
    printed = forms.CharField(label="Impression",
                            required=False,
                            widget=forms.Select(
                               choices=PRINTED,
                               attrs={
                                   "class": "form-control",
                               }
                           ))
    # status = forms.CharField(label="Etat",
    #                         required=False,
    #                         widget=forms.Select(
    #                            choices=COIL_STATUS,
    #                            attrs={
    #                                "class": "form-control",
    #                            }
    #                        ))
    type_coil = forms.ModelChoiceField(
        label="Type",
        queryset=CoilType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))     
    perfume = forms.CharField(label="Parfum",
                           widget=forms.Select(
                               choices=PERFUMED,
                               attrs={
                                   "class": "form-control",
                               }
                           ))
    flavor = forms.ModelChoiceField(
        label="Parfum",
        required=False,
        queryset=Flavor.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))             
    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data


class ProductionForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = [
        "product",
        "coil_type",
        "quantity_produced",
        "machine",
        ]
    
    product = forms.ModelChoiceField(
        required=False,
        label="Produit",
        queryset=FinishedProductType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))

    coil_type = forms.ModelChoiceField(
        required=False,
        label="Bobine",
        queryset=CoilType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))

    quantity_produced = forms.IntegerField(
                            label="Quantité",
                            required=False,
                            widget=forms.TextInput(
                                  attrs={
                                      "class": "form-control",
                                      "type": "number",
                                  }
                              ))

    machine = forms.ModelChoiceField(
        label="Machine",
        queryset=Machine.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class CoilDetailForm(forms.ModelForm):
    
    weight = forms.FloatField(max_value=500, 
    widget=forms.TextInput(
            attrs={
            "class": "form-control",
            "type" : "number ",
            'step' : '0.01',
            'min'  : "0"
            }

        )
    )
    micronnage = forms.FloatField(max_value=500, 
    widget=forms.TextInput(
            attrs={
            "class": "form-control",
            "type" : "number ",
            'step' : '0.01',
            'min'  : "0"
            }

        )
    )
    class Meta:
        model = Coil
        fields = ["weight","micronnage"]

class ShapingForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['machine','user']
    user = forms.ModelChoiceField(
        label="Opérateur",
        queryset=User.objects.filter(profile__job_position__name = "Opérateur Façonnage"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    machine = forms.ModelChoiceField(
        label="Soudeuse",
        queryset=Machine.objects.filter(Q(machine_type__name="Soudeuse")),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class PrintingForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = [ 'machine', 'the_print']

    machine = forms.ModelChoiceField(
        label="Imprimeuse",
        queryset=Machine.objects.filter(Q(machine_type__name="Imprimeuse")),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    the_print = forms.CharField(label="Impression",
                           widget=forms.Select(
                               choices=PRINT_CHOICES,
                               attrs={
                                   "class": "form-control",
                               }
                           ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class FinishedProductForm(forms.ModelForm):
    class Meta:
        model = Production
        fields = ['user', 'user2', 'user3', 'product', 'machine', 'quantity_produced']
    user = forms.ModelChoiceField(
        label="Opérateur 1",
        queryset=User.objects.filter(profile__job_position__name = "Opérateur Façonnage"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
        
        )
    user2 = forms.ModelChoiceField(
        label="Opérateur 2",
        required=False,
        queryset=User.objects.filter(profile__job_position__name = "Opérateur Façonnage"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
        
        )
    user3 = forms.ModelChoiceField(
        label="Opérateur 3",
        required=False,
        queryset=User.objects.filter(profile__job_position__name = "Opérateur Façonnage"),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
        
        )
    product = forms.ModelChoiceField(
        label="Produit",
        queryset=FinishedProductType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        )
        
        )

    machine = forms.ModelChoiceField(
        label="Soudeuse",
        queryset=Machine.objects.filter(Q(machine_type__name="Soudeuse")),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    quantity_produced = forms.IntegerField(label="Quantité du Produit",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  )) 
    

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class ExtrusionTrashForm(forms.ModelForm):
    class Meta:
        model = Trash
        fields = ['trash_type', 'machine', 'weight']

    trash_type = forms.CharField(label="Type Déchet",
                           widget=forms.Select(
                               choices=TYPE_TRASH,
                               attrs={
                                   "class": "form-control",
                               }
                           ))

    machine = forms.ModelChoiceField(
        label="Machine",
        queryset=Machine.objects.filter(Q(machine_type__name="Extrudeuse") | Q(machine_type__name="Imprimeuse")),
        widget=forms.Select(
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
                                          'step' : '0.01',
                                          'min'  : "0"
                                      }
                                  )) 
    

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data


class ShapingTrashForm(forms.ModelForm):
    class Meta:
        model = Trash
        fields = ['trash_type', 'machine', 'weight']

    trash_type = forms.CharField(label="Type Déchet",
                           widget=forms.Select(
                               choices=TYPE_TRASH,
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
    weight = forms.FloatField(label="Poids Déchet",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'step' : '0.01',
                                          'min'  : "0"
                                      }
                                  )) 
    

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class PrintingTrashForm(forms.ModelForm):
    class Meta:
        model = Trash
        fields = ['trash_type', 'machine', 'weight']

    trash_type = forms.CharField(label="Type Déchet",
                           widget=forms.Select(
                               choices=TYPE_TRASH,
                               attrs={
                                   "class": "form-control",
                               }
                           ))

    machine = forms.ModelChoiceField(
        label="Machine",
        queryset=Machine.objects.filter(Q(machine_type__name="Imprimeuse")),
        widget=forms.Select(
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
                                          'step' : '0.01',
                                          'min'  : "0"
                                      }
                                  )) 
    

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class GeneralTrashForm(forms.ModelForm):
    class Meta:
        model = Trash
        fields = ['trash_type', 'machine', 'weight', 'comment']

    trash_type = forms.CharField(label="Type Déchet",
                           widget=forms.Select(
                               choices=TYPE_TRASH,
                               attrs={
                                   "class": "form-control",
                               }
                           ))

    machine = forms.ModelChoiceField(
        required=False,
        label="Machine",
        queryset=Machine.objects.filter(Q(machine_type__name="Extrudeuse")) | Machine.objects.filter(Q(machine_type__name="Imprimeuse")) | Machine.objects.filter(Q(machine_type__name="Soudeuse")),
        widget=forms.Select(
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
                                          'step' : '0.01',
                                          'min'  : "0"
                                      }
                                  )) 
    
    comment = forms.CharField(label="Source",
                           widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                               }
                           ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data


class HandleConsumptionForm(forms.ModelForm):
    class Meta:
        model = HandleConsumption
        fields = ['handle', 'machine', 'quantity']

    handle = forms.ModelChoiceField(label="Cordon",
                            queryset=Handle.objects.filter(quantity_workshop__gt=0),
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
    quantity = forms.IntegerField(label="Nombre de rouleaux",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  )) 
    

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class LabellingConsumptionForm(forms.ModelForm):
    class Meta:
        model = LabellingConsumption
        fields = ['labelling', 'machine', 'quantity']

    labelling = forms.ModelChoiceField(label="Labelling",
                            queryset=Labelling.objects.filter(quantity_workshop__gt=0),
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
    quantity = forms.IntegerField(label="Nombre de rouleaux",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  )) 
    

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data


class InkConsumptionForm(forms.ModelForm):
    class Meta:
        model = InkConsumption
        fields = ['ink', 'machine', 'quantity']

    ink = forms.ModelChoiceField(label="Encre",
                            queryset=RawMatter.objects.filter(name__name="encre"),
                            widget=forms.Select(   
                               attrs={
                                   "class": "form-control",
                               }
                           ))

    machine = forms.ModelChoiceField(
        label="Machine",
        queryset=Machine.objects.filter(Q(machine_type__name="Imprimeuse")),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    quantity = forms.FloatField(label="Quantité",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'step' : '0.01',
                                          'min'  : "0"
                                      }
                                  )) 
    

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data


class ExtrusionMachineStopForm(forms.ModelForm):
    class Meta:
        model = MachineStop
        fields = ['machine', 'hours','minutes', 'cause', 'comment']

    machine = forms.ModelChoiceField(
        label="Machine",
        queryset=Machine.objects.filter(Q(machine_type__name="Extrudeuse") | Q(machine_type__name="Imprimeuse")),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    hours = forms.IntegerField(label="Heures",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  ))
    minutes = forms.IntegerField(label="Minutes",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  ))

    cause = forms.CharField(label="Cause",
                           widget=forms.Select(
                               choices=MACHINE_STOP,
                               attrs={
                                   "class": "form-control",
                               }
        )
        )
    comment = forms.CharField(label="Commentaire",
                            required=False,
                            widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                               }
        )
        )

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class PrintingMachineStopForm(forms.ModelForm):
    class Meta:
        model = MachineStop
        fields = ['machine', 'hours','minutes', 'cause', 'comment']

    machine = forms.ModelChoiceField(
        label="Machine",
        queryset=Machine.objects.filter(Q(machine_type__name="Imprimeuse")),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    hours = forms.IntegerField(label="Heures",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  ))
    minutes = forms.IntegerField(label="Minutes",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  ))

    cause = forms.CharField(label="Cause",
                           widget=forms.Select(
                               choices=MACHINE_STOP,
                               attrs={
                                   "class": "form-control",
                               }
        )
        )
    comment = forms.CharField(label="Commentaire",
                            required=False,
                            widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                               }
        )
        )

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class ShapingMachineStopForm(forms.ModelForm):
    class Meta:
        model = MachineStop
        fields = ['machine', 'hours','minutes', 'cause', 'comment']

    machine = forms.ModelChoiceField(
        label="Machine",
        queryset=Machine.objects.filter(Q(machine_type__name="Soudeuse")),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    hours = forms.IntegerField(label="Heures",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  ))
    minutes = forms.IntegerField(label="Minutes",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  ))

    cause = forms.CharField(label="Cause",
                           widget=forms.Select(
                               choices=MACHINE_STOP,
                               attrs={
                                   "class": "form-control",
                               }
        )
        )
    comment = forms.CharField(label="Commentaire",
                            required=False,
                            widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                               }
        )
        )

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class MixingMachineStopForm(forms.ModelForm):
    class Meta:
        model = MachineStop
        fields = ['machine', 'hours','minutes', 'cause', 'comment']

    machine = forms.ModelChoiceField(
        label="Machine",
        queryset=Machine.objects.filter(Q(machine_type__name="Mélangeur")),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    hours = forms.IntegerField(label="Heures",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  ))
    minutes = forms.IntegerField(label="Minutes",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'min'  : "0"
                                      }
                                  ))

    cause = forms.CharField(label="Cause",
                           widget=forms.Select(
                               choices=MACHINE_STOP,
                               attrs={
                                   "class": "form-control",
                               }
        )
        )
    comment = forms.CharField(label="Commentaire",
                            required=False,
                            widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                               }
        )
        )

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data