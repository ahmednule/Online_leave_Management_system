from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['role', 'department']
        # Add widgets or customizations if needed
        widgets = {
            'role': forms.TextInput(attrs={'class': 'form-control'}),
            'department': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'address']
        # Add widgets or customizations if needed
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Add custom validation for phone number if needed
        return phone_number

    def clean_address(self):
        address = self.cleaned_data.get('address')
        # Add custom validation for address if needed
        return address
