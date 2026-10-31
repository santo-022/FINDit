from django import forms
from .models import Item


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item

        fields = [
            'title',
            'catagory',
            'description',
            'picture',
            'color',
            'brand',
            'location',
            'incident_d_t',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item name'
            }),

            'catagory': forms.Select(attrs={
                'class': 'form-select'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the item'
            }),

            'picture': forms.ClearableFileInput(attrs={
                'class': 'form-control'
            }),

            'color': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item color'
            }),

            'brand': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Item brand (write N/A if unknown)'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Where was it lost or found?'
            }),

            'incident_d_t': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }