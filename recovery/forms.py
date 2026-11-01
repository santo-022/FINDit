from django import forms
from .models import ClaimRequest


class ClaimRequestForm(forms.ModelForm):

    class Meta:
        model = ClaimRequest
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Explain why you believe this item belongs to you...'
            })
        }

        labels = {
            'comment': 'Why is this your item?'
        }
