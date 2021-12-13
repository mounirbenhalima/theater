from django import forms

from .models import Company


class CompanyForm(forms.ModelForm):
    name = forms.CharField(
        label="Nom de l'Entrerprise",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))
    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "email",
            }
        ))
    fax = forms.EmailField(
        label="Fax",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))
    mobile = forms.EmailField(
        label="Téléphone",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))
    address = forms.EmailField(
        label="Adresse",
        required=True,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "type": "text",
            }
        ))

    class Meta:
        model = Company
        fields = '__all__'
