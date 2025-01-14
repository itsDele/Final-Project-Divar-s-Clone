from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm, UsernameField
from django import forms
from django.utils.translation import gettext as _
from .models import UserProfile, Ad, AdImage

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = ("username", "first_name", "last_name", "email", "phone")
        labels = {
            "first_name": "First Name",
            "last_name": "Last Name",
            "email": "Email",
            "phone": "Phone Number"
        }
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.NumberInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
        }

class MyUserUpdateForm(UserChangeForm):
    class Meta:
        model = UserProfile
        fields = ("username", "first_name", "last_name", "email", "phone")

class SignInForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.TextInput(attrs={"autofocus": True, "class": "form-control"})
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(
            attrs={"autocomplete": "current-password", "class": "form-control"}
        ),
    )

class AdListingForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'price', 'publication_date', 'ad_category', 'city_location']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'city_location': forms.Select(attrs={'class': 'form-control'}),
            'ad_category': forms.Select(attrs={'class': 'form-control'}),
        }

class AdImageForm(forms.ModelForm):
    class Meta:
        model = AdImage
        fields = ('image_file',)
        widgets = {
            'image_file': forms.ClearableFileInput(attrs={'multiple': True, 'accept': 'image/*'}),
        }

    def save(self, ad_listing, *args, **kwargs):
        uploaded_images = self.files.getlist('image_file')
        for image in uploaded_images:
            AdImage.objects.create(ad_listing=ad_listing, image_file=image)