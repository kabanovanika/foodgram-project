import enum
from typing import Iterable, List, Optional

from recipe.models import Favorite, Recipe, ShoppingList


class Tag(str, enum.Enum):
    BREAKFAST = 'breakfast'
    LUNCH = 'lunch'
    DINNER = 'dinner'


EVERY_TAG = [member.value for member in Tag]


def get_ingredients_for_recipe_form(query_data):
    ingredients = [
        query_data[key] for key in query_data.keys()
        if key.startswith('nameIngredient')
    ]
    amounts = [
        query_data[key] for key in query_data.keys()
        if key.startswith('valueIngredient')
    ]

    result = zip(ingredients, amounts)

    return result


def get_recipes_with_tags(tags: List[str],
                          author_id: Optional[int] = None,
                          recipe_id_seq: Optional[Iterable[int]] = None):
    query = Recipe.objects

    if recipe_id_seq is not None:
        query = query.filter(id__in=recipe_id_seq)

    if author_id is not None:
        query = query.filter(author=author_id)

    if tags:
        return query.filter(tags__in=tags).distinct()
    return query.all()


def recipe_is_favorite(user_id, recipe_id):
    return Favorite.objects.filter(
        user_id__exact=user_id, favorite_recipe_id__exact=recipe_id).exists()


def recipe_in_shop_list(user_id, recipe_id):
    return ShoppingList.objects.filter(
        user_id__exact=user_id, purchase_recipe_id__exact=recipe_id).exists()


def get_filter_values(request):
    filter_values = [f for f in EVERY_TAG if request.GET.get(f) == 'off']
    return filter_values


def get_page_content(request):
    page_number = request.GET.get('page')
    return page_number


def conjugate_recipes(count: int) -> str:
    remainder = count % 10

    if count in (11, 12, 13, 14):
        return 'рецептов'

    if remainder == 1:
        return 'рецепт'

    if remainder in (2, 3, 4):
        return 'рецепта'

    return 'рецептов'
