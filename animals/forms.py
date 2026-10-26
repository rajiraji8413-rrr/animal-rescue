from django import forms
from django.contrib.auth.models import User

from .models import Animal, AdoptionRequest


class AnimalAdminForm(forms.ModelForm):

    class Meta:
        model = Animal
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        species = cleaned_data.get('species')
        breed = cleaned_data.get('breed')

        if species and breed:
            if breed.species != species:
                raise forms.ValidationError(
                    'The selected breed does not belong to the selected species.'
                )

        return cleaned_data


class AdoptionRequestForm(forms.ModelForm):

    class Meta:
        model = AdoptionRequest
        fields = ['message']

        labels = {
            'message': 'Why would you like to adopt this animal?',
        }

        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 5,
                'placeholder': (
                    'Tell us why you would like to adopt this animal...'
                ),
            }),
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email Address',
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Enter your first name',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Enter your last name',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address',
            }),
        }
