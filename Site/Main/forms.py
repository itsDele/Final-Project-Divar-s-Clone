from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from django import forms
from django.contrib.auth.models import MyUser  # Renamed User model
from django.utils.translation import gettext, gettext_lazy as _
from .models import MyUser as MyCustomUserModel, AdListing, AdImage
from .widgets import CustomWidgets  # Assume you want to keep widgets custom

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = MyCustomUserModel
        fields = ("user_username", "user_firstname", "user_surname", "user_email", "user_phone")
        labels = {
            "user_firstname": "First Name",
            "user_surname": "Last Name",
            "user_email": "Email",
            "user_phone": "Phone Number"
        }
        widgets = {
            "user_username": forms.TextInput(attrs={"class": "form-control"}),
            "user_firstname": forms.TextInput(attrs={"class": "form-control"}),
            "user_phone": forms.NumberInput(attrs={"class": "form-control"}),
            "user_surname": forms.TextInput(attrs={"class": "form-control"}),
            "user_email": forms.EmailInput(attrs={"class": "form-control"}),
        }

class MyUserUpdateForm(UserChangeForm):
    class Meta:
        model = MyCustomUserModel
        fields = ("user_username", "user_firstname", "user_surname", "user_email", "user_phone")

class RegistrationForm(MyUserCreationForm):
    user_password1 = forms.CharField(
        label="Password", widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    user_password2 = forms.CharField(
        label="Confirm Password (again)",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    class Meta:
        model = MyCustomUserModel
        fields = ("user_username", "user_firstname", "user_surname", "user_email")
        labels = {
            "user_firstname": "First Name",
            "user_surname": "Last Name",
            "user_email": "Email",
            "user_phone": "Phone Number"
        }
        widgets = {
            "user_username": forms.TextInput(attrs={"class": "form-control"}),
            "user_firstname": forms.TextInput(attrs={"class": "form-control"}),
            "user_phone": forms.NumberInput(attrs={"class": "form-control"}),
            "user_surname": forms.TextInput(attrs={"class": "form-control"}),
            "user_email": forms.EmailInput(attrs={"class": "form-control"}),
        }

class SignInForm(AuthenticationForm):
    user_name = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    user_password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )

class AdListingForm(forms.ModelForm):
    class Meta:
        model = AdListing
        fields = ['ad_title', 'ad_description', 'ad_price', 'ad_date', 'ad_category', 'ad_location']
        widgets = {
            'ad_title': forms.TextInput(attrs={'class': 'form-control'}),
            'ad_description': forms.Textarea(attrs={'class': 'form-control'}),
            'ad_price': forms.NumberInput(attrs={'class': 'form-control'}),
            'ad_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'ad_location': forms.Select(attrs={'class': 'form-control'}),
            'ad_category': forms.Select(attrs={'class': 'form-control'}),
        }

class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImage
        fields = ('ad_image_file',)
        widgets = {
            'ad_image_file': CustomWidgets.MultiFileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        }

    def save(self, ad_listing, *args, **kwargs):
        uploaded_images = self.files.getlist('ad_image_file')
        for image in uploaded_images:
            AdImage.objects.create(ad_listing=ad_listing, ad_image_file=image)