from django import forms
from . models import Machine, MachineType
from Product.models import Brand


class MachineForm(forms.ModelForm):
    model_name = forms.CharField(label="Modèle",
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
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

    machine_type = forms.ModelChoiceField(
        label="Type de la machine",
        queryset=MachineType.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control col mr-1",
            }
        ))
    machine_number = forms.CharField(label="Numéro",
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
                                     }
                                 ))
                                 

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

    class Meta:
        model = Machine
        fields = '__all__'
        exclude = ('slug',)


class MachineTypeForm(forms.ModelForm):
    name = forms.CharField(label="Type de machine",
                           required=True,
                           widget=forms.TextInput(
                               attrs={
                                   "class": "form-control",
                                   "type": "text",
                               }
                           ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

    class Meta:
        exclude = ('slug',)
        model = MachineType
        fields = "__all__"
