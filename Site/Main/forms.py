from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import User, Advertising, AdvertisingImage, Category
from .widgets import *

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone_number")
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "phone_number": "Phone Number"
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone_number": forms.NumberInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

class CustomUserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "phone_number")

class AdvertisingForm(forms.ModelForm):
    class Meta:
        model = Advertising
        fields = ['title', 'description', 'price', 'publication_date', 'category', 'city']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }

class AdvertisingImageForm(forms.ModelForm):
    class Meta:
        model = AdvertisingImage
        fields = ('image',)
        widgets = {
            'image': MultiFileInputWidget(attrs={'multiple': True, 'accept': 'image/*'}),
        }

    def save(self, advertisement, *args, **kwargs):
        images = self.files.getlist('image')
        for image in images:
            AdvertisingImage.objects.create(advertisement=advertisement, image=image)