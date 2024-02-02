from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import CustomUser, Property, Location
from django import forms


class CustomUserCreationForm(UserCreationForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), max_length=250, required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields =("first_name", "last_name", "phone_number", "username",
                 "email", "password1", "password2", "bio", "profile_pic")


class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']


class CustomUserChangeForm(UserChangeForm):
    bio = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), max_length=250, required=False)
    profile_pic = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "phone_number", "username",
                  "email", "bio", "profile_pic")


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = ['state', 'city', 'district', 'postal_code', 'street', 'house_number']


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['title', 'description', 'price', 'category', 'status', 'image_1', 'image_2', 'image_3']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.location_form = LocationForm(*args, **kwargs)

    def is_valid(self):
        # Check the validity of both the main and embedded forms
        return super().is_valid() and self.location_form.is_valid()

    def save(self, commit=True, *args, **kwargs):
        # Save both forms
        instance = super().save(commit=False, *args, **kwargs)
        location_instance = self.location_form.save(commit=False)

        # Assign the location to the property
        instance.location = location_instance

        if commit:
            instance.save()
            location_instance.save()

        return instance
