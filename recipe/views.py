# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse

from .forms import RecipeForm
from .models import Recipe, Ingredient


def index(request):
    recipes = Recipe.objects.all()
    paginator = Paginator(recipes, 5)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'indexAuth.html', {
        'page': page,
        'paginator': paginator
    })


def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)

    if request.method == 'POST':
        if form.is_valid():
            if request.user.is_authenticated:
                recipe = Recipe(**form.cleaned_data, author=request.user)
                recipe.save()
                return redirect('/')
            return redirect('/auth/login')

    return render(request, "formRecipe.html", {"form": form})
