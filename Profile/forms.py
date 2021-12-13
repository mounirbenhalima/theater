from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, JobPosition, HolidayRequest, Point, HOLIDAY_MOTIVES
from Company.models import Company

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(
        label="Prénom",
        max_length=255,
        required=True,
        widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "text",

        }
    ))
    last_name = forms.CharField(
        label="Nom",
        max_length=255,
        required=True,
        widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "text",
        }
    ))
    username = forms.CharField(
        label="Pseudo",
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
            "id": "email",
        }
    ))
    password1 = forms.CharField(
        label="Mot de Passe",
        widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "password",
            "id": "password",

        }
    ))
    password2 = forms.CharField(
        label="Confirmer Mot de Passe",
        widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "password",
            "id": "password",
        }
    ))

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
            'first_name',
            'last_name']

""" """
class ProfileForm(forms.ModelForm):
    job_position = forms.ModelChoiceField(
        label="Intitulé du Poste",
        queryset=JobPosition.objects.all(),
        required=False,
        widget=forms.Select(
            attrs={
                "class":"form-control",
            }
        
    ))
    group = forms.IntegerField(
        label="Groupe",
        required=True,
        widget=forms.TextInput(
            attrs={
                "type":"number",
                "class":"form-control",
            }
        
    ))
    salary = forms.FloatField(
        label="Salaire de base",
        required=False,
        widget=forms.TextInput(
            attrs={
                "type":"number",
                "class":"form-control",
            }
        
    ))
    
    bonus = forms.FloatField(
        label="Pourcentage Prime",
        required=False,
        widget=forms.TextInput(
            attrs={
                "type":"number",
                "class":"form-control",
            }
        
    ))

    birth_day = forms.DateField(
        label="Date de Naissance",
        required=False,
        widget=forms.DateInput(
        attrs={
            "class": "form-control",
            "type": "date"
        }
    ))

    hiring_date = forms.DateField(
        label="Date de Recrutement",
        required=False,
        widget=forms.DateInput(
        attrs={
            "class": "form-control",
            "type": "date"
        }
    ))
    rest_holiday = forms.IntegerField(
        label="Jours de Congé Restants",
        required=True,
        widget=forms.TextInput(
            attrs={
                "type":"number",
                "class":"form-control",
            }
        
    ))
    mobile = forms.CharField(
        required=False,
        label='Numéro de Téléphone',
        widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "text",

        }
    ))
    address = forms.CharField(
        required=False,
        label='Adresse',
        widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "text",

        }
    ))

    # image = forms.ImageField(required=False)

    self_transported = forms.BooleanField(label = "Transport Personnel", required=False)

    active = forms.BooleanField(label = "Élément Actif", required=False)


    class Meta:
        model = Profile
        exclude = ('slug','user')
        fields = [
                'birth_day',
                'job_position',
                'group',
                'salary',
                'bonus',
                'hiring_date',
                'rest_holiday',
                'mobile',
                'address',
                # 'image', 
                'self_transported', 
                'active', 
                ]


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "text",

        }
    ))

    password = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "password",
            "id":"password",
        }
    ))
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

class JobPositionForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "text",

        }
    ))
    class Meta:
        model = JobPosition
        exclude = ('slug',)
        fields = '__all__'

class DateInput(forms.DateInput):
    input_type='date'

class HolidayRequestForm(forms.ModelForm):
    class Meta:
        model = HolidayRequest
        fields = ['start_date', 'end_date', 'address', 'mobile', 'motive', 'substitute']

    start_date = forms.DateField(
        label="Date Début De Congé",
        widget=DateInput(
            attrs={
                "class": "form-control",
            }
        ))
    end_date = forms.DateField(
        label="Date Fin De Congé",
        widget=DateInput(
            attrs={
                "class": "form-control",
            }
        ))
    
    address = forms.CharField(
        required=True,
        widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "text",

        }
    ))

    mobile = forms.CharField(
        required=True,
        label='Numéro de Téléphone',
        max_length=10,
        widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "type": "text",

        }
    ))

    motive = forms.CharField(
        required=True,
        label="Motif",
        widget=forms.Select(
        choices=HOLIDAY_MOTIVES,
        attrs={
            "class": "form-control",
        }
    ))

    substitute = forms.ModelChoiceField(
        label="Remplaçant",
        queryset=User.objects.all(),
        required=True,
        widget=forms.Select(
        attrs={
            "class": "form-control",
        }
    ))
    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data

class PointForm(forms.ModelForm):
    class Meta:
        model = Point
        fields = ['start_date', 'end_date','absence', 'holiday']


    start_date = forms.DateField(
        label="Date Début",
        widget=DateInput(
            attrs={
                "class": "form-control",
            }
        ))
    end_date = forms.DateField(
        label="Date Fin",
        widget=DateInput(
            attrs={
                "class": "form-control",
            }
        ))

    absence = forms.FloatField(label="Absence",
                                  required=False,
                                  widget=forms.TextInput(
                                      attrs={
                                          "class": "form-control",
                                          "type": "number",
                                          'step' : '0.01',
                                          'min'  : "0"
                                      }
                                  ))
    # holiday = forms.ChoiceField(widget=forms.RadioSelect, choices=[('True', 'Congé'), ('False', 'Non')])
    holiday =forms.CharField(label='Congé',required = False, widget=forms.RadioSelect(choices=[(True,"Congé")]))


    def clean(self):
        cleaned_data = super().clean()
        return self.cleaned_data