from django import forms
from .models import Ticket

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['price']
    price = forms.FloatField(label="Tarif",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          "step":"0.01",
                                      }
                                  ))

    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data