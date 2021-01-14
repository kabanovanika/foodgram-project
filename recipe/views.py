# from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .forms import RecipeForm
from .models import Recipe, Ingredient, RecipeIngredient
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
import json
from django.http import JsonResponse


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_ingredients(request):
    query = request.GET.get('query')
    queryset = Ingredient.objects.filter(title__startswith=query)
    ing_list = []
    for item in queryset:
        dict_response = {"title": item.title, "dimension": item.dimension}
        ing_list.append(dict_response)
    return JsonResponse(ing_list, safe=False)


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
    form = RecipeForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            if request.user.is_authenticated:
                recipe = Recipe(**form.cleaned_data, author=request.user)
                recipe.save()
                i = 1
                for field in form.data:
                    if field.startswith('nameIngredient_'):
                        recipe_ingredient = request.POST[f'nameIngredient_{i}']
                        amount = request.POST[f'valueIngredient_{i}']
                        k = Ingredient.objects.get(title=recipe_ingredient)
                        RecipeIngredient.objects.create(recipe_id=recipe.pk,
                                                        ingredient=Ingredient.objects.get(title=recipe_ingredient),
                                                        amount=amount)
                        i += 1
                return redirect('/')
            return redirect('/auth/login')
    return render(request, "formRecipe.html", {"form": form, })


def subscriptions(request):
    return render(request, "myFollow.html")


def recipe_page(request, recipe_id):
    recipe = get_object_or_404(Recipe,
                               id__exact=recipe_id)
    author = recipe.author
    cooking_time = recipe.cooking_time
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    description = recipe.text
    return render(request, "singlePageNotAuth.html", {
        "recipe": recipe,
        "author": author,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "description": description,

    })

#
# if request.user.is_authenticated:
#     recipe = Recipe(**form.cleaned_data, author=request.user)
#     recipe.save()
#     i = 1
#     for field in form.data:
#         if field.startswith('nameIngredient_'):
#             recipe_ingredient = request.POST[f'nameIngredient_{i}']
#             amount = request.POST[f'valueIngredient_{i}']
#             RecipeIngredient.objects.create(recipe_id=recipe.pk,
#                                             ingredient=Ingredient.objects.get(title=recipe_ingredient),
#                                             amount=amount)
#             i += 1


# def new_recipe(request):
#     form = RecipeForm(request.POST)
#     print('я сюда зашел')
#     print(form.data)
#     print(request.POST.dict())
#     if request.method == 'POST':
#         if form.is_valid():
#             print('форма валидна')
#             if request.user.is_authenticated:
#                 recipe = Recipe(**form.cleaned_data, author=request.user)
#                 recipe.save()
#                 return redirect('/')
#             return redirect('/auth/login')
#     return render(request, "formRecipe.html", {"form": form, })
