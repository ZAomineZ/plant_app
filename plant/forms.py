from django import forms
from django.utils.text import slugify

from plant.models import Category, Plant

SHADE = [
    (slugify('Plein ombre'), 'Plein ombre'),
    (slugify('Semi ombre'), 'Semi ombre'),
    (slugify('Plein soleil'), 'Plein soleil')
]
MOISTURE = [
    (slugify('Sol sec'), 'Sol sec'),
    (slugify('Sol humide'), 'Sol humide'),
    (slugify('Sol humide ou marécageux'), 'Sol humide ou marécageux'),
    (slugify('Plantes aquatiques'), 'Plantes aquatiques'),
    (slugify('Bien drainée'), 'Bien drainée'),
    (slugify('Résiste à la chaleur'), 'Résiste à la chaleur')
]
WIND = [
    (slugify('Exposition maritime'), 'Exposition maritime'),
    (slugify('Tolèrant au vent fort'), 'Tolèrant au vent fort'),
    (slugify('Non tolèrant au vent'), 'Non tolèrant au vent')
]
SOIL = [
    (slugify('Léger (sableux)'), 'Léger (sableux)'),
    (slugify('Moyen'), 'Moyen'),
    (slugify('Lourd'), 'Lourd'),
    (slugify('Argile lourde'), 'Argile lourde'),
    (slugify('Sol pauvre'), 'Sol pauvre')
]
GROWTH_RATE = [(slugify('Vite'), 'Vite'), (slugify('Moyen'), 'Moyen'), (slugify('Lent'), 'Lent')]


class PlantForm(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=60, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.CharField(label="Slug", max_length=60, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))

    shade = forms.CharField(label="Type d'ombre", max_length=50, required=False,
                            widget=forms.Select(attrs={'class': 'form-control'}, choices=SHADE))
    moisture = forms.CharField(label="Type d'humidité", max_length=50, required=False,
                               widget=forms.Select(attrs={'class': 'form-control'}, choices=MOISTURE))
    wind = forms.CharField(label="Type de vent", max_length=50, required=False,
                           widget=forms.Select(attrs={'class': 'form-control'}, choices=WIND))
    soil = forms.CharField(label="Type de sol", max_length=50, required=False,
                           widget=forms.Select(attrs={'class': 'form-control'}, choices=SOIL))
    growth_rate = forms.CharField(label="Taux de croissance", max_length=50, required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}, choices=GROWTH_RATE))

    image = forms.ImageField(required=False, label="Image", widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Plant
        fields = ('title', 'slug', 'description', 'category')


class PlantFilterForm(forms.Form):
    search_plant = forms.CharField(label="Chercher une plante", max_length=60, required=False,
                                   widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Chercher une plante...'}))
    search_category = forms.ModelChoiceField(Category.objects.all(),
                                             widget=forms.Select(attrs={'class': 'form-control'}), required=False)

    search_shade = forms.CharField(label="Chercher par type d'ombre", max_length=50, required=False,
                                   widget=forms.Select(attrs={'class': 'form-control'}, choices=SHADE))
    search_moisture = forms.CharField(label="Chercher par type d'humidité", max_length=50, required=False,
                                      widget=forms.Select(attrs={'class': 'form-control'}, choices=MOISTURE))
    search_wind = forms.CharField(label="Chercher par type de vent", max_length=50, required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}, choices=WIND))
    search_soil = forms.CharField(label="Chercher par type de sol", max_length=50, required=False,
                                  widget=forms.Select(attrs={'class': 'form-control'}, choices=SOIL))
    search_growth_rate = forms.CharField(label="Taux de croissance", max_length=50, required=False,
                                         widget=forms.Select(attrs={'class': 'form-control'}, choices=GROWTH_RATE))


class CategoryForm(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=60, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.CharField(label="Slug", max_length=60, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Category
        fields = ('title', 'slug', 'description')
