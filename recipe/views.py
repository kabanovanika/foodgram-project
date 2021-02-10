import json
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer

from foodgram import settings

from . import domain
from .domain.user import DomainUser
from .forms import RecipeForm
from .models import (Favorite, Follow, Ingredient, Recipe, RecipeIngredient,
                     ShoppingList, Tag, User)


def page_not_found(request, exception):
    return render(request, 'misc/404.html', {'path': request.path}, status=404)


def server_error(request):
    return render(request, 'misc/500.html', status=500)


@api_view(('GET',))
@renderer_classes((TemplateHTMLRenderer, JSONRenderer))
def get_ingredients(request):
    query = request.GET.get('query')
    queryset = Ingredient.objects.filter(title__startswith=query)
    ingredient_list = []
    if not queryset.exists():
        ingredient_list = [{
            'title': 'Такого ингредиента не существует',
            'dimension': ''
        }]
        return JsonResponse(ingredient_list, safe=False)
    for item in queryset:
        dict_response = {'title': item.title, 'dimension': item.dimension}
        ingredient_list.append(dict_response)
    return JsonResponse(ingredient_list, safe=False)


def index(request):
    image = Recipe.image
    filter_values = domain.get_filter_values(request)
    tags = []
    if filter_values:
        tags = Tag.objects.exclude(slug__in=filter_values)
    recipes = domain.get_recipes_with_tags(tags)
    paginator = Paginator(recipes, settings.ITEMS_PER_PAGE)
    page_number = domain.get_page_content(request)
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'image': image,
        'is_user_authenticated': request.user.is_authenticated
    }

    if request.user.is_authenticated:
        domain_user = DomainUser(request.user.id)
        context['in_shop_list'] = domain_user.shopping_list()
        context['in_favorite'] = domain_user.favorites()

    return render(request, 'index.html', context)


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    ingredients = domain.get_ingredients_for_recipe_form(request.POST)
    if form.is_valid():
        if request.user.is_authenticated:
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            for (item, amount) in ingredients:
                RecipeIngredient.objects.create(
                    ingredient=get_object_or_404(Ingredient,
                                                 title__exact=item),
                    amount=amount,
                    recipe=recipe,
                )
            form.save_m2m()
            return redirect('index')
        return redirect('login')
    return render(request, 'formRecipe.html', {
        'form': form,
        'is_user_authenticated': request.user.is_authenticated,
    })


def recipe_page(request, recipe_id):
    recipe = get_object_or_404(Recipe, id__exact=recipe_id)
    image = recipe.image
    author = recipe.author
    cooking_time = recipe.cooking_time
    ingredients = RecipeIngredient.objects.filter(recipe_id=recipe_id)
    description = recipe.text

    context = {
        'is_user_authenticated': request.user.is_authenticated,
        'recipe': recipe,
        'author': author,
        'image': image,
        'cooking_time': cooking_time,
        'ingredients': ingredients,
        'description': description,
    }

    if request.user.is_authenticated:
        domain_user = DomainUser(request.user.id)
        context['is_favorite'] = domain.recipe_is_favorite(
            request.user, recipe.id)
        context['in_shop_list'] = domain.recipe_in_shop_list(
            request.user, recipe.id)
        context['following'] = domain_user.is_following(author=author)

    return render(request, 'singlePage.html', context)


@login_required
def recipe_edit(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    if request.user != recipe.author:
        return redirect('index')
    form = RecipeForm(request.POST or None,
                      files=request.FILES or None,
                      instance=recipe)
    if request.POST.get('delete') == '':
        recipe.delete()
        return redirect('index')
    ingredients = domain.get_ingredients_for_recipe_form(request.POST)
    if form.is_valid():
        RecipeIngredient.objects.filter(recipe=recipe).delete()
        recipe = form.save(commit=False)
        recipe.author = request.user
        recipe.save()
        for (item, amount) in ingredients:
            RecipeIngredient.objects.create(
                ingredient=get_object_or_404(Ingredient, title__exact=item),
                amount=amount,
                recipe=recipe,
            )
        form.save_m2m()
        return redirect('index')
    return render(
        request,
        'formChangeRecipe.html',
        {
            'form': form,
            'recipe': recipe,
            'recipe_id': recipe_id,
            'is_user_authenticated': request.user.is_authenticated,
        },
    )


def profile(request, username):
    user = get_object_or_404(User, username__exact=username)
    user_id = user.id
    user_name = user.first_name
    filter_values = domain.get_filter_values(request)
    tags = []
    if filter_values:
        tags = Tag.objects.exclude(slug__in=filter_values)
    recipes = domain.get_recipes_with_tags(tags, author_id=user_id)
    paginator = Paginator(recipes, settings.ITEMS_PER_PAGE)
    image = Recipe.image
    page_number = domain.get_page_content(request)
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'paginator': paginator,
        'image': image,
        'is_user_authenticated': request.user.is_authenticated,
        'user_id': user_id,
    }

    if request.user.is_authenticated:
        domain_user = DomainUser(request.user.id)
        context['in_shop_list'] = domain_user.shopping_list()
        context['in_favorite'] = domain_user.favorites()
        context['name'] = user_name

    return render(request, 'authorRecipe.html', context)


@login_required
@csrf_exempt
def profile_follow(request):
    authors_queryset = Follow.objects.values_list('author', flat=True).filter(
        user=request.user).order_by('-id')
    authors = [f for f in authors_queryset]
    recipes_from_author_id = {
        author: Recipe.objects.filter(author__exact=author)[:3]
        for author in authors
    }
    recipe_count_from_author_id = {
        author: Recipe.objects.filter(author__exact=author).count() - 3
        for author in authors
    }
    paginator = Paginator(authors_queryset, settings.ITEMS_PER_PAGE)
    page_number = domain.get_page_content(request)
    page = paginator.get_page(page_number)
    return render(
        request, 'myFollow.html', {
            'is_user_authenticated': True,
            'authors': authors,
            'recipes_from_author_id': recipes_from_author_id,
            'recipe_count_from_author_id': recipe_count_from_author_id,
            'page': page,
            'paginator': paginator,
        })


class Purchases(LoginRequiredMixin, View):
    def post(self, request):
        request_data = json.loads(request.body)
        recipe_id = request_data.get('id')
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id__exact=recipe_id)
            ShoppingList.objects.get_or_create(user=request.user,
                                               purchase_recipe=recipe)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)

    def delete(self, request, recipe_id):
        purchase_recipe = get_object_or_404(ShoppingList,
                                            purchase_recipe=recipe_id,
                                            user=request.user)
        purchase_recipe.delete()
        return JsonResponse({'success': True})


@login_required()
def purchases_list(request):
    recipes_id = ShoppingList.objects.values_list(
        'purchase_recipe_id', flat=True).filter(user__exact=request.user)
    recipes = Recipe.objects.filter(id__in=recipes_id)
    image = Recipe.image
    return render(request, 'shopList.html', {
        'is_user_authenticated': True,
        'recipes': recipes,
        'image': image,
    })


def shop_list_file(request):
    recipes_id = ShoppingList.objects.values_list(
        'purchase_recipe_id', flat=True).filter(user__exact=request.user)
    recipes = Recipe.objects.filter(id__in=recipes_id)
    raw_shop_list = list(
        RecipeIngredient.objects.filter(recipe__in=recipes).values(
            'ingredient_id', 'amount'))
    shop_dict = defaultdict(int)
    for item in range(len(raw_shop_list)):
        ingredient_id = raw_shop_list[item]['ingredient_id']
        ingredient_amount = raw_shop_list[item]['amount']
        shop_dict[ingredient_id] += ingredient_amount
    final_shop_list = ['Список продуктов:']
    for ingredient_id, ingredient_amount in shop_dict.items():
        ingredient = get_object_or_404(Ingredient, id__exact=ingredient_id)
        full_ingredient_info = (f'{ingredient} - {ingredient_amount}'
                                f' ({ingredient.dimension})')
        final_shop_list.append(full_ingredient_info)
    file_data = '\n'.join(final_shop_list)
    response = HttpResponse(file_data,
                            content_type='application/text charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="to_buy.txt"'
    return response


class Favorites(LoginRequiredMixin, View):
    def post(self, request):
        request_data = json.loads(request.body)
        recipe_id = request_data.get('id')
        if recipe_id is not None:
            recipe = get_object_or_404(Recipe, id__exact=recipe_id)
            Favorite.objects.get_or_create(user=request.user,
                                           favorite_recipe=recipe)
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)

    def delete(self, request, recipe_id):
        favorite_recipe = get_object_or_404(Favorite,
                                            favorite_recipe=recipe_id,
                                            user=request.user)
        favorite_recipe.delete()
        return JsonResponse({'success': True})


def favorite_recipes(request):
    domain_user = DomainUser(request.user.id)
    favorite_recipe_ids = domain_user.favorites()
    filter_values = domain.get_filter_values(request)
    tags = []
    if filter_values:
        tags = Tag.objects.exclude(slug__in=filter_values)
    recipes = domain.get_recipes_with_tags(tags,
                                           recipe_id_seq=favorite_recipe_ids)
    image = Recipe.image
    paginator = Paginator(recipes, settings.ITEMS_PER_PAGE)
    page_number = domain.get_page_content(request)
    page = paginator.get_page(page_number)
    in_shop_list = domain_user.shopping_list()
    context = {
        'recipes': recipes,
        'page': page,
        'paginator': paginator,
        'image': image,
        'is_user_authenticated': request.user.is_authenticated,
        'in_shop_list': in_shop_list,
        'in_favorite': favorite_recipe_ids,
    }

    return render(request, 'favorite.html', context)


class Subscriptions(LoginRequiredMixin, View):
    def post(self, request):
        request_data = json.loads(request.body)
        user_id = request_data.get('id')
        if user_id is not None:
            author = get_object_or_404(User, id__exact=user_id)
            if request.user != author:
                Follow.objects.get_or_create(author=author, user=request.user)
                return JsonResponse({'success': True})
            return JsonResponse({'success': True})
        return JsonResponse({'success': False}, status=400)

    def delete(self, request, author):
        follower = get_object_or_404(Follow, author=author, user=request.user)
        follower.delete()
        return JsonResponse({'success': True})
