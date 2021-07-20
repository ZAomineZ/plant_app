from django import forms

from plant.models import Category, Plant


class PlantForm(forms.ModelForm):
    title = forms.CharField(label="Title", max_length=60, required=True,
                            widget=forms.TextInput(attrs={'class': 'form-control'}))
    slug = forms.CharField(label="Slug", max_length=60, required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))
    category = forms.ModelChoiceField(Category.objects.all(), widget=forms.Select(attrs={'class': 'form-control'}))
    image = forms.ImageField(required=True, label="Image", widget=forms.FileInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Plant
        fields = ('title', 'slug', 'description', 'category')
