from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify

from plant.forms import CategoryForm
from plant.models import Category


def categories(request):
    categories = Category.objects.all()
    return render(request, 'admin/categories/index.html', {'categories': categories})


def categories_create(request):
    errors = None

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            # Save new category
            slug = slugify(title)
            Category.objects.create(title=title, slug=slug, description=description)

            messages.success(request, 'Tu as crée ta catégorie avec success !')
            return HttpResponseRedirect(reverse('admin:categories'))
        else:
            errors = form.errors
    else:
        form = CategoryForm()
    return render(request, 'admin/categories/create.html', {'form': form, 'errors': errors})


def categories_edit(request, category_id: int):
    category = get_object_or_404(Category, pk=category_id)
    errors = None

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            slug = slugify(title)
            description = form.cleaned_data['description']
            # Save new category
            category.title = title
            category.slug = slug
            category.description = description
            category.save()

            messages.success(request, 'Tu as édité ta catégorie avec success !')
            return HttpResponseRedirect(reverse('admin:categories'))
        else:
            errors = form.errors
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin/categories/edit.html', {
        'form': form,
        'category': category,
        'errors': errors
    })
