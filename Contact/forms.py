from django import forms
from . models import Contact, CONTACT_TYPE


class ContactForm(forms.ModelForm):
    first_name = forms.CharField(label="Prénom",
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
                                     }
                                 ))
    last_name = forms.CharField(label="Nom",
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
                                     }
                                 ))
    contact_type = forms.CharField(label="Type du Contact",
                                widget=forms.Select(
                                    choices=CONTACT_TYPE,
                                    attrs={
                                        "class": "form-control",
                                    }
                                ))
    email = forms.EmailField(label="Email",
        required=False,
        widget=forms.TextInput(
         attrs={
             "class": "form-control",
             "type": "email",
         }
     ))
    

    phone_number = forms.CharField(label="Téléphone",
                                 required=False,
                                 widget=forms.TextInput(
                                     attrs={
                                         "class": "form-control",
                                         "type": "text",
                                     }
                                 ))
    address = forms.CharField(label="Adresse",
                                 required=False,
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
        model = Contact
        fields = ['first_name', 'last_name', 'contact_type', 'email', "phone_number", "address"]