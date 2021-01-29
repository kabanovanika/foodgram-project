import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from . import domain
from .domain.user import DomainUser
from .forms import RecipeForm
from .models import Recipe, Ingredient, RecipeIngredient, Favorite, User, Follow, Tag, ShoppingList
from rest_framework.decorators import api_view, renderer_classes
from django.contrib.auth.decorators import login_required
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from collections import defaultdict


def page_not_found(request, exception):
    return render(
        request,
        "misc/404.html",
        {"path": request.path},
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)


def amount_purchases(request):
    counter = ShoppingList.objects.values_list('purchase_recipe_id', flat=True).filter(user_id=request.user)
    amount = len(counter)
    if amount == 0:
        amount = ''
    return amount


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


def get_ingredients_for_recipe_form(query_data):
    ingredients = [
        query_data[key]
        for key in query_data.keys()
        if key.startswith("nameIngredient")
    ]
    amounts = [
        query_data[key]
        for key in query_data.keys()
        if key.startswith("valueIngredient")]

    result = zip(ingredients, amounts)

    return result


def index(request):
    image = Recipe.image
    filters = ['breakfast', 'lunch', 'dinner']
    filter_values = [f for f in filters if request.GET.get(f) == 'off']
    tags = []
    if filter_values:
        tags = Tag.objects.exclude(slug__in=filter_values)
    recipes = domain.get_recipes_with_tags(tags)
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:
        in_shop_list = ShoppingList.objects.values_list('purchase_recipe_id', flat=True).filter(user_id=request.user)
        in_favorite = Favorite.objects.values_list('favorite_recipe_id', flat=True).filter(user_id=request.user)
        counter = amount_purchases(request)
        return render(request, 'indexAuth.html', {
            'page': page,
            'paginator': paginator,
            'image': image,
            'in_shop_list': in_shop_list,
            'in_favorite': in_favorite,
            'counter': counter,
        })
    else:
        return render(request, 'indexNotAuth.html', {
            'page': page,
            'paginator': paginator,
            'image': image,
        })


@login_required
def new_recipe(request):
    counter = amount_purchases(request)
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    if request.method == 'POST':
        ingredients = get_ingredients_for_recipe_form(request.POST)

        if form.is_valid():
            if request.user.is_authenticated:
                recipe = form.save(commit=False)
                recipe.author = request.user
                recipe.save()
                for (item, amount) in ingredients:
                    RecipeIngredient.objects.create(
                        ingredient=Ingredient.objects.get(title=f"{item}"),
                        amount=amount,
                        recipe=recipe,
                    )
                form.save_m2m()
                return redirect('index')
            return redirect('/auth/login')
    return render(request, "formRecipe.html", {"form": form, "counter": counter})


class Subscriptions(LoginRequiredMixin, View):

    def post(self, request):
        reg = json.loads(request.body)
        user_id = reg.get("id", None)
        if user_id is not None:
            author = get_object_or_404(User, id__exact=user_id)
            if request.user != author:
                Follow.objects.get_or_create(author=author, user=request.user)
                return JsonResponse({"success": True})
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, author):
        follower = get_object_or_404(
            Follow, author=author, user=request.user)
        follower.delete()
        return JsonResponse({"success": True})


def recipe_page(request, recipe_id):
    recipe = get_object_or_404(Recipe,
                               id__exact=recipe_id)
    image = recipe.image
    author = recipe.author
    cooking_time = recipe.cooking_time
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    description = recipe.text
    if request.user.is_authenticated:
        is_favorite = Favorite.objects.filter(user_id__exact=request.user,
                                              favorite_recipe_id__exact=recipe.id).exists()
        in_shop_list = ShoppingList.objects.filter(user_id__exact=request.user,
                                                   purchase_recipe_id__exact=recipe.id).exists()
        following = Follow.objects.filter(user_id__exact=request.user, author_id__exact=author).exists()
        counter = amount_purchases(request)
        return render(request, "singlePage.html", {
            "recipe": recipe,
            "author": author,
            "image": image,
            "cooking_time": cooking_time,
            "ingredients": ingredients,
            "description": description,
            'following': following,
            'in_shop_list': in_shop_list,
            'is_favorite': is_favorite,
            'counter': counter,

        })
    else:
        return render(request, "singlePageNotAuth.html", {
            "recipe": recipe,
            "author": author,
            "image": image,
            "cooking_time": cooking_time,
            "ingredients": ingredients,
            "description": description,

        })


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect("index")
    form = RecipeForm(
        request.POST or None, files=request.FILES or None, instance=recipe
    )
    if request.method == "POST":
        if request.POST.get('delete') == '':
            recipe.delete()
            return redirect('index')
        ingredients = get_ingredients_for_recipe_form(request.POST)
        if form.is_valid():
            RecipeIngredient.objects.filter(recipe=recipe).delete()
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for (item, amount) in ingredients:
                RecipeIngredient.objects.create(
                    ingredient=Ingredient.objects.get(title=f"{item}"),
                    amount=amount,
                    recipe=recipe,
                )
            form.save_m2m()
        return redirect('index')

    return render(
        request, "formChangeRecipe.html", {"form": form, "recipe": recipe, "recipe_id": recipe_id, },
    )


def profile(request, username):
    user = get_object_or_404(User, username__exact=username)
    user_id = user.id
    user_name = user.first_name
    filters = ['breakfast', 'lunch', 'dinner']
    filter_values = [f for f in filters if request.GET.get(f) == 'off']
    tags = []
    if filter_values:
        tags = Tag.objects.exclude(slug__in=filter_values)
    recipes = domain.get_recipes_with_tags(tags, author_id=user_id)
    paginator = Paginator(recipes, 6)
    image = Recipe.image
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    if request.user.is_authenticated:
        following = Follow.objects.filter(user_id__exact=request.user, author_id__exact=user_id).exists()
        in_shop_list = ShoppingList.objects.values_list('purchase_recipe_id', flat=True).filter(user_id=request.user)
        in_favorite = Favorite.objects.values_list('favorite_recipe_id', flat=True).filter(user_id=request.user)
        counter = amount_purchases(request)
        return render(request, "authorRecipe.html", {
            'user_id': user_id,
            'page': page,
            'paginator': paginator,
            'image': image,
            'name': user_name,
            'in_shop_list': in_shop_list,
            'in_favorite': in_favorite,
            'counter': counter,
            'following': following,
        })
    else:
        return render(request, "authorRecipeNotAuth.html", {
            'page': page,
            'paginator': paginator,
            'image': image,
            'name': user_name,
        })


@login_required
@csrf_exempt
def profile_follow(request):
    authors = [f.author for f in Follow.objects.filter(user=request.user).all()]
    recipes_from_author_id = {a.id: Recipe.objects.filter(author__exact=a)[:3] for a in authors}
    recipe_count_from_author_id = {a.id: Recipe.objects.filter(author__exact=a).count() - 3 for a in authors}
    paginator = Paginator(authors, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    counter = amount_purchases(request)
    return render(request, 'myFollow.html', {
        'authors': authors,
        'recipes_from_author_id': recipes_from_author_id,
        'recipe_count_from_author_id': recipe_count_from_author_id,
        'page': page,
        'paginator': paginator,
        'counter': counter,
    })


class Purchases(LoginRequiredMixin, View):

    def post(self, request):
        reg = json.loads(request.body)
        recipe_id = reg.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id__exact=recipe_id)
            ShoppingList.objects.get_or_create(user=request.user, purchase_recipe=recipe)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        purchase_recipe = get_object_or_404(
            ShoppingList, purchase_recipe=recipe_id, user=request.user)
        purchase_recipe.delete()
        return JsonResponse({"success": True})


@login_required()
def purchases_list(request):
    recipes_id = ShoppingList.objects.values_list('purchase_recipe_id', flat=True).filter(user__exact=request.user)
    recipes = Recipe.objects.filter(id__in=recipes_id)
    image = Recipe.image
    counter = amount_purchases(request)
    return render(request, "shopList.html", {
        'recipes': recipes,
        'image': image,
        'counter': counter,
    })


def my_view(request):
    recipes_id = ShoppingList.objects.values_list('purchase_recipe_id', flat=True).filter(user__exact=request.user)
    recipes = Recipe.objects.filter(id__in=recipes_id)
    raw_shop_list = list(RecipeIngredient.objects.filter(recipe__in=recipes).values('ingredient_id', 'amount'))
    d = []
    for i in range(len(raw_shop_list)):
        k = raw_shop_list[i]['ingredient_id']
        v = raw_shop_list[i]['amount']
        d.append((k, v))
    shop_dict = defaultdict(int)
    for k, v in d:
        shop_dict[k] += v
    final_shop_list = ['Список продуктов:']
    for k, v in shop_dict.items():
        ingredient_name = Ingredient.objects.values_list('title', flat=True).get(id=k)
        ingredient_dimension = Ingredient.objects.values_list('dimension', flat=True).get(id=k)
        full_ingredient_info = f'{ingredient_name} - {v} ({ingredient_dimension})'
        final_shop_list.append(full_ingredient_info)
    file_data = '\n'.join(final_shop_list)
    response = HttpResponse(file_data, content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="to_buy.txt"'
    return response


class Favorites(LoginRequiredMixin, View):

    def post(self, request):
        reg = json.loads(request.body)
        recipe_id = reg.get("id", None)
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id__exact=recipe_id)
            Favorite.objects.get_or_create(user=request.user, favorite_recipe=recipe)
            return JsonResponse({"success": True})
        return JsonResponse({"success": False}, status=400)

    def delete(self, request, recipe_id):
        favorite_recipe = get_object_or_404(
            Favorite, favorite_recipe=recipe_id, user=request.user)
        favorite_recipe.delete()
        return JsonResponse({"success": True})


def favorite_recipes(request):
    counter = amount_purchases(request)
    domain_user = DomainUser(request.user.id)
    favorite_recipe_ids = domain_user.favorites()
    filters = ['breakfast', 'lunch', 'dinner']
    filter_values = [f for f in filters if request.GET.get(f) == 'off']
    tags = []
    if filter_values:
        tags = Tag.objects.exclude(slug__in=filter_values)
    recipes = domain.get_recipes_with_tags(tags, recipe_id_seq=favorite_recipe_ids)
    image = Recipe.image
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    in_shop_list = domain_user.shopping_list()
    return render(request, "favorite.html", {
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'image': image,
        'in_shop_list': in_shop_list,
        'in_favorite': favorite_recipe_ids,
        'counter': counter,
    })
