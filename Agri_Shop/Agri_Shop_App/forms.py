from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import HighQualitySeed, OrganicFertilizer, SafePesticide, FarmEquipment, AnimalFeed, AgriElectronicsTool


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1','password2']


class UserUpdationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name']

MODEL_MAPPING = {
    'HighQualitySeed': HighQualitySeed,
    'OrganicFertilizer': OrganicFertilizer,
    'SafePesticide': SafePesticide,
    'FarmEquipment': FarmEquipment,
    'AnimalFeed': AnimalFeed,
    'AgriElectronicsTool': AgriElectronicsTool,
}

def get_product_form(product_type):
    class ProductForm(forms.ModelForm):
        class Meta:
            model = MODEL_MAPPING[product_type]  
            fields = '__all__'
    return ProductForm
