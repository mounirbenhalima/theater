from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile, JobPosition
from Company.models import Company

class DateInput(forms.DateInput):
    input_type='date'

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


    class Meta:
        model = Profile
        exclude = ('slug','user')
        fields = [
                'job_position', 
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