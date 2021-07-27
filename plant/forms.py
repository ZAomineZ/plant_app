from django import forms
from django.utils.text import slugify

from plant.models import Category, Plant, CustomUser

SHADE = [
    (slugify(''), 'Chosir une option...'),
    (slugify('Plein ombre'), 'Plein ombre'),
    (slugify('Semi ombre'), 'Semi ombre'),
    (slugify('Plein soleil'), 'Plein soleil')
]
MOISTURE = [
    (slugify(''), 'Chosir une option...'),
    (slugify('Sol sec'), 'Sol sec'),
    (slugify('Sol humide'), 'Sol humide'),
    (slugify('Sol humide ou marécageux'), 'Sol humide ou marécageux'),
    (slugify('Plantes aquatiques'), 'Plantes aquatiques'),
    (slugify('Bien drainée'), 'Bien drainée'),
    (slugify('Résiste à la chaleur'), 'Résiste à la chaleur')
]
WIND = [
    (slugify(''), 'Chosir une option...'),
    (slugify('Exposition maritime'), 'Exposition maritime'),
    (slugify('Tolèrant au vent fort'), 'Tolèrant au vent fort'),
    (slugify('Non tolèrant au vent'), 'Non tolèrant au vent')
]
SOIL = [
    (slugify(''), 'Chosir une option...'),
    (slugify('Léger (sableux)'), 'Léger (sableux)'),
    (slugify('Moyen'), 'Moyen'),
    (slugify('Lourd'), 'Lourd'),
    (slugify('Argile lourde'), 'Argile lourde'),
    (slugify('Sol pauvre'), 'Sol pauvre')
]
GROWTH_RATE = [(slugify(''), 'Chosir une option...'), (slugify('Vite'), 'Vite'), (slugify('Moyen'), 'Moyen'),
               (slugify('Lent'), 'Lent')]


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
                                   widget=forms.TextInput(
                                       attrs={'class': 'form-control', 'placeholder': 'Chercher une plante...'}))
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


class RegisterForm(forms.ModelForm):
    username = forms.CharField(label='username', max_length=255, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.CharField(label='email', max_length=255, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', max_length=255, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_confirm = forms.CharField(label='password', max_length=255, required=True,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def clean_email(self):
        return self.validator_field_exist('email')

    def clean_username(self):
        return self.validator_field_exist('username')

    def clean(self):
        clean_data = super().clean()
        password = clean_data.get('password')
        password_confirm = clean_data.get('password_confirm')
        if password is not None and password != password_confirm:
            self.add_error('password', 'Vos mot de passes doivent être identiques.')
        return clean_data

    def validator_field_exist(self, field: str):
        field_data = self.cleaned_data.get(field)
        field_data_exist = CustomUser.objects.filter(**{field: field_data})
        if field_data_exist.exists():
            self.add_error(field, 'L\'{} est dèjà pris'.format(field))
        return field_data


class LoginForm(forms.Form):
    username = forms.CharField(label='username', max_length=255, required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='password', max_length=255, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user = CustomUser.objects.filter(username=username)
        if not user.exists():
            self.add_error('username', 'Cette username n\'éxiste pas dans notre base de donnée'.format('username'))
        return username
