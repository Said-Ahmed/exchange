from django import forms
from .models import Ad

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image_url', 'category', 'condition']


class AdSearchForm(forms.Form):
    search = forms.CharField(
        required=False,
        max_length=100,
        label='Поиск'
    )
    category = forms.ChoiceField(
        choices=Ad.CATEGORY_CHOICES,
        required=False,
        label='Категория'
    )
    condition = forms.ChoiceField(
        choices=Ad.CONDITION_CHOICES,
        required=False,
        label='Состояние'
    )