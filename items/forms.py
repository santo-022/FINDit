
from django import forms
from .models import Item


BUILDING_CHOICES = [
    ('Main Building', 'Main Building'),
    ('RH Building', 'RH Building'),
]

FLOOR_CHOICES = [
    ('2', '2nd Floor'),
    ('3', '3rd Floor'),
    ('4', '4th Floor'),
    ('5', '5th Floor'),
    ('6', '6th Floor'),
    ('7', '7th Floor'),
    ('8', '8th Floor'),
]

FLOOR_NAMES = {
    '2nd Floor': '2',
    '3rd Floor': '3',
    '4th Floor': '4',
    '5th Floor': '5',
    '6th Floor': '6',
    '7th Floor': '7',
    '8th Floor': '8',
}


class ItemForm(forms.ModelForm):

    building = forms.ChoiceField(
        choices=BUILDING_CHOICES,
        label='Building',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    floor = forms.ChoiceField(
        choices=FLOOR_CHOICES,
        label='Floor',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    location_detail = forms.ChoiceField(
        choices=[],
        label='Room / Lab',
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Item
        fields = [
            'title',
            'catagory',
            'description',
            'picture',
            'color',
            'brand',
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
            'incident_d_t': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        building = None
        floor = None
        location_detail = None

        # Get existing location for Update page
        if self.instance and self.instance.pk:
            parts = self.instance.location.split(' - ')

            if len(parts) == 3:
                building = parts[0]
                floor = FLOOR_NAMES.get(parts[1])
                location_detail = parts[2]

        # Get submitted values
        if self.is_bound:
            building = self.data.get('building')
            floor = self.data.get('floor')
            location_detail = self.data.get('location_detail')

        if building:
            self.fields['building'].initial = building

        if floor:
            self.fields['floor'].initial = floor

        if floor and floor.isdigit() and 2 <= int(floor) <= 8:

            floor_number = int(floor)

            choices = [
                (f'Room {floor_number}{room:02d}',
                 f'Room {floor_number}{room:02d}')
                for room in range(1, 4)
            ]

            choices += [
                (f'Lab {lab:02d}', f'Lab {lab:02d}')
                for lab in range(1, 5)
            ]

            self.fields['location_detail'].choices = choices

            if location_detail:
                self.fields['location_detail'].initial = location_detail

    def clean(self):
        cleaned_data = super().clean()

        floor = cleaned_data.get('floor')
        location_detail = cleaned_data.get('location_detail')

        if floor and location_detail:
            if location_detail.startswith('Room'):
                expected_prefix = f'Room {floor}'

                if not location_detail.startswith(expected_prefix):
                    self.add_error(
                        'location_detail',
                        'Please select a room from the selected floor.'
                    )

        return cleaned_data

    def save(self, commit=True):
        item = super().save(commit=False)

        floor = self.cleaned_data['floor']

        ordinal = {
            '2': '2nd',
            '3': '3rd',
            '4': '4th',
            '5': '5th',
            '6': '6th',
            '7': '7th',
            '8': '8th',
        }[floor]

        item.location = (
            f"{self.cleaned_data['building']} - "
            f"{ordinal} Floor - "
            f"{self.cleaned_data['location_detail']}"
        )

        if commit:
            item.save()

        return item
