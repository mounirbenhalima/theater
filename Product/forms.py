from django import forms
from .choices import PRINT_CHOICES, TYPE_PRODUCT, TYPE_PIECE, TAPE_TYPE, TYPE_TRASH,PERFUMED, RANGE_CATEGORY, SIZE
from .models import (
    Brand,
    Color,
    Flavor,
    Product,
    Coil,
    RawMatter,
    FinishedProduct,
    Range,
    CombinedRange,
    CoilType,
    Handle,
    Labelling,
    Package,
    FinishedProductType,
    Tape,
    SparePart
)
from StockManager.models import Warehouse
from Contact.models import Contact


class BrandForm(forms.ModelForm):
    name = forms.CharField(
        label="Nom de La Marque",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['name'] = cleaned_data['name'].lower()
        return self.cleaned_data

    class Meta:
        model = Brand
        exclude = ('slug',)
        fields = "__all__"

class RangeForm(forms.ModelForm):
    name = forms.CharField(
        label="Nom de La Gamme",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['name'] = cleaned_data['name'].lower()
        return self.cleaned_data

    class Meta:
        model = Range
        exclude = ('slug',)
        fields = "__all__"

class CombinedRangeForm(forms.ModelForm):
    class Meta:
        model = CombinedRange
        fields = ['range_name', 'capacity', 'the_print', 'perfume', 'color', 'type_name', 'category']

    range_name = forms.ModelChoiceField(
        queryset=Range.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    
    color = forms.ModelChoiceField(
        label="Couleur",
        required=False,
        queryset=Color.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    capacity = forms.CharField(
                            required=False,
                            label="Taille",
                           widget=forms.Select(
                               choices=SIZE,
                               attrs={
                                   "class": "form-control",
                               }
                           ))
    the_print = forms.CharField(
                            required=False,
                            label="Impression",
                           widget=forms.Select(
                               choices=PRINT_CHOICES,
                               attrs={
                                   "class": "form-control",
                               }
                           ))
    
    category = forms.CharField(
                            label="Catégorie",
                           widget=forms.Select(
                               choices=RANGE_CATEGORY,
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

    type_name = forms.CharField(
                            required=False,
                            label="Type",
                           widget=forms.Select(
                               choices=TYPE_PRODUCT,
                               attrs={
                                   "class": "form-control",
                               }
                           ))
    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class ColorForm(forms.ModelForm):
    name = forms.CharField(label="Nom de La Couleur",
                           required=True,
                           widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                                   "type": "text",
                               }
                           ))

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['name'] = cleaned_data['name'].lower()
        return self.cleaned_data

    class Meta:
        model = Color
        exclude = ('slug',)
        fields = "__all__"

class FlavorForm(forms.ModelForm):
    name = forms.CharField(label="Parfum",
                           required=True,
                           widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                                   "type": "text",
                               }
                           ))

    def clean(self):
        cleaned_data = super().clean()
        self.cleaned_data['name'] = cleaned_data['name'].lower()
        return self.cleaned_data

    class Meta:
        model = Flavor
        exclude = ('slug',)
        fields = "__all__"

class RawMatterForm(forms.ModelForm):
    class Meta:
        model = RawMatter
        fields = ['name', 'combined_range', 'weight','ref', 'type_name','perfume', 'brand', 'color', 'flavor', 'price']
    name = forms.ModelChoiceField(
        label="Gamme",
        queryset=Range.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    #combined_range = forms.ModelChoiceField(
    #    queryset=CombinedRange.objects.all(),
    #    widget=forms.Select(
    #        attrs={
    #            "class": "form-control",
    #        }
    #    ))
    flavor = forms.ModelChoiceField(
        label="Parfum",
        required=False,
        queryset=Flavor.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    weight = forms.IntegerField(label="Poids Unitaire",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                      }
                                  ))
    price = forms.FloatField(label="Prix Unitaire",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          "step":"0.1",
                                      }
                                  ))
    type_name = forms.CharField(label="Type",
                                widget=forms.Select(
                                    choices=TYPE_PRODUCT,
                                    attrs={
                                        "class": "form-control",
                                    }
                                ))
    ref = forms.CharField(label="Référence",
                                widget=forms.TextInput(
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
    brand = forms.ModelChoiceField(
        label="Marque",
        queryset=Brand.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
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

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data


class CoilTypeForm(forms.ModelForm):
    class Meta:
        model = CoilType
        fields = [
            'name',
            'ref',
            'capacity',
            'micronnage_ideal',
            'quantity',
            'type_name',
            'warehouse',
            'brand',
            'color',
            'the_print',
            'perfume',
            'flavor',
            'width',
        ]
    name = forms.ModelChoiceField(label="Nom de la bobine",
                                  queryset=Range.objects.all(),
                                  widget=forms.Select(
                                      attrs={
                                          "class": "form-control",
                                      }
                                  ))
    capacity = forms.CharField(
                            required=False,
                            label="Taille",
                           widget=forms.Select(
                               choices=SIZE,
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
    the_print = forms.CharField(label="Impression",
                           widget=forms.Select(
                               choices=PRINT_CHOICES,
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
    quantity = forms.IntegerField(label="Quantité en stock",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                      }
                                  ))
    micronnage_ideal = forms.FloatField(label="Micronnage idéal",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          "step":"0.1",
                                      }
                                  ))
    type_name = forms.CharField(label="Type de la bobine",
                                widget=forms.Select(
                                    choices=TYPE_PRODUCT,
                                    attrs={
                                        "class": "form-control",
                                    }
                                ))
    width = forms.FloatField(label="Largeur de la bobine",
                            required=False,
                             widget=forms.TextInput(
                                 attrs={
                                     "type": "number",
                                     "class": "form-control",
                                 }
                             ))
    warehouse = forms.ModelChoiceField(label="Entrepôt",
                                        required=False,
                                       queryset=Warehouse.objects.all(),
                                       widget=forms.Select(
                                           attrs={
                                               "class": "form-control",
                                           }
                                       ))
    brand = forms.ModelChoiceField(label="Marque",
                                    required=False,
                                   queryset=Brand.objects.all(),
                                   widget=forms.Select(
                                       attrs={
                                           "class": "form-control",
                                       }
                                   ))
    color = forms.ModelChoiceField(label="Couleur",
                                    required=False,
                                   queryset=Color.objects.all(),
                                   widget=forms.Select(
                                       attrs={
                                           "class": "form-control",
                                       }
                                   ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class FinalProductForm(forms.ModelForm):
    class Meta:
        model = FinishedProductType
        fields = ['name', 'ref','package','bag_roll','roll_package', 'capacity', 'quantity', 'height', 'width', 'weight', 'the_print','type_name', 'color','perfume','flavor' ,'price']

    name = forms.ModelChoiceField(
        label="Gamme",
        queryset=Range.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    # combined_range = forms.ModelChoiceField(
    #     label="Gamme Combinées",
    #     queryset=CombinedRange.objects.all(),
    #     widget=forms.Select(
    #         attrs={
    #             "class": "form-control",
    #         }
    #     ))
    flavor = forms.ModelChoiceField(
        label="Parfum",
        required=False,
        queryset=Flavor.objects.all(),
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
    capacity = forms.CharField(
                            required=False,
                            label="Taille",
                           widget=forms.Select(
                               choices=SIZE,
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
    quantity = forms.IntegerField(label="Quantité en Stock",
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                      }
                                  ))
    weight = forms.FloatField(label="Poids idéal",
                              required=True,
                              widget=forms.TextInput(
                                  attrs={
                                      "class": "form-control",
                                      "type": "number",
                                  }
                              ))
    price = forms.FloatField(label="Prix Unitaire",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          "step":"0.1",
                                      }
                                  ))
    height = forms.FloatField(label="Longueur du sac",
                              required=False,
                              widget=forms.TextInput(
                                  attrs={
                                      "class": "form-control",
                                      "type": "number",
                                  }
                              ))
    width = forms.FloatField(label="Largeur du sac",
                             required=False,
                             widget=forms.TextInput(
                                 attrs={
                                     "class": "form-control",
                                     "type": "number",
                                 }
                             ))
    type_name = forms.CharField(label="Type du Produit",
                                widget=forms.Select(
                                    choices=TYPE_PRODUCT,
                                    attrs={
                                        "class": "form-control",
                                    }
                                ))
    
    package = forms.ModelChoiceField(
        label="Emballage",
        required=False,
        queryset=Package.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    bag_roll = forms.IntegerField(label="Sacs/Rouleau",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                      }
                                  ))
    roll_package = forms.IntegerField(label="Rouleaux/Carton",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                      }
                                  ))
    color = forms.ModelChoiceField(
        required=False,
        queryset=Color.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class HandleForm(forms.ModelForm):
    class Meta:
        model = Handle
        fields = ['brand', 'color' ]
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    color = forms.ModelChoiceField(
        queryset=Color.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class LabellingForm(forms.ModelForm):
    class Meta:
        model = Labelling
        fields = [ 'name','capacity', 'the_print', 'perfume' ]

    name = forms.ModelChoiceField(
        queryset=Range.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    capacity = forms.CharField(
                            required=False,
                            label="Taille",
                           widget=forms.Select(
                               choices=SIZE,
                               attrs={
                                   "class": "form-control",
                               }
                           ))
    the_print = forms.CharField(
        required=True,
        label="Impression",
        widget=forms.Select(
            choices=PRINT_CHOICES,
            attrs={
                "class": "form-control",
            }
        ))
    perfume = forms.CharField(
        required=True,
        label="Parfum",
        widget=forms.Select(
            choices=PERFUMED,
            attrs={
                "class": "form-control",
            }
        ))
    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data


class PackageForm(forms.ModelForm):
    class Meta:
        model = Package
        fields = ['name','capacity','the_print','perfume' ]
    name = forms.ModelChoiceField(
        queryset=Range.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    capacity = forms.CharField(
                            required=False,
                            label="Taille",
                           widget=forms.Select(
                               choices=SIZE,
                               attrs={
                                   "class": "form-control",
                               }
                           ))
    the_print = forms.CharField(
        required=True,
        label="Impression",
        widget=forms.Select(
            choices=PRINT_CHOICES,
            attrs={
                "class": "form-control",
            }
        ))
    perfume = forms.CharField(
        required=True,
        label="Parfum",
        widget=forms.Select(
            choices=PERFUMED,
            attrs={
                "class": "form-control",
            }
        ))
    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class TapeForm(forms.ModelForm):
    class Meta:
        model = Tape
        fields = ['brand','tape_type' ]
    brand = forms.ModelChoiceField(
        required=False,
        queryset=Brand.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control",
            }
        ))
    tape_type = forms.CharField(
        label="Type",
        widget=forms.Select(
            choices=TAPE_TYPE,
            attrs={
                "class": "form-control",
            }
        ))
    

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class SparePartForm(forms.ModelForm):
    class Meta:
        model = SparePart
        fields = ['name','name_fr','ref', 'quantity', 'price', 'category', 'threshold' ]
    
    ref = forms.CharField(
        label="Référence",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))
    

    name = forms.CharField(
        label="Désignation ENG",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))
    
    name_fr = forms.CharField(
        label="Désignation FR",
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))

    category = forms.CharField(
        label="Catégorie",
        widget=forms.Select(
            choices=TYPE_PIECE,
            attrs={
                "class": "form-control",
            }
        ))

    quantity = forms.IntegerField(label="Quantité en Stock",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                      }
                                  ))
    threshold = forms.IntegerField(label="Seuil Minimal",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                      }
                                  ))
    price = forms.FloatField(label="Prix",
                                  required=True,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          "step":"0.1",
                                      }
                                  ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data