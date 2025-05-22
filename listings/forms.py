from django import forms

from .choices import state_choices
from .models import Listing
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator


class ListingForm(forms.ModelForm):
    state = forms.ChoiceField(
        choices=state_choices.items(),
        widget=forms.Select(attrs={
            'class': 'form-control rounded-pill px-3',
        }),
        label='Область'
    )
    class Meta:
        model = Listing
        fields = ['title', 'address', 'city', 'state', 'zipcode',
                  'description', 'price', 'bedrooms', 'bathrooms',
                  'garage', 'sqft', 'lot_size', 'photo_main',
                  'photo_1', 'photo_2', 'photo_3', 'photo_4',
                  'photo_5', 'photo_6', 'is_published']

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control rounded-pill px-3',
                'placeholder': 'Введите название'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control rounded-pill px-3',
                'placeholder': 'Введите адрес'
            }),
            'price': forms.TextInput(attrs={
                'class': 'form-control rounded-pill px-3 price-input',
                'placeholder': 'Цена в долларах',
                'inputmode': 'numeric'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control rounded-3',
                'rows': 5,
                'placeholder': 'Опишите особенности недвижимости'
            }),
            'city': forms.TextInput(attrs={
                'class': 'form-control rounded-pill px-3',
                'placeholder': 'Введите город'
            }),
            'zipcode': forms.TextInput(attrs={
                'class': 'form-control rounded-pill px-3',
                'placeholder': 'Введите год постройки',
                'min': 1900,
                'max': datetime.now().year,
                'type': 'number',
                'value': 2025
            }),
            'bedrooms': forms.NumberInput(attrs={
                'class': 'form-control rounded-pill px-3',
                'placeholder': 'Количество комнат'
            }),
            'bathrooms': forms.NumberInput(attrs={
                'class': 'form-control rounded-pill px-3',
                'placeholder': 'Количество санузлов'
            }),
            'garage': forms.NumberInput(attrs={
                'class': 'form-control rounded-pill px-3',
                'placeholder': 'Количество гаражей'
            }),
            'sqft': forms.NumberInput(attrs={
                'class': 'form-control rounded-pill px-3',
                'placeholder': 'Площадь (м²)'
            }),
            'lot_size': forms.NumberInput(attrs={
                'class': 'form-control rounded-pill px-3',
                'placeholder': 'Площадь участка (соток)'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_published'].widget = forms.HiddenInput()
        self.fields['is_published'].initial = False

