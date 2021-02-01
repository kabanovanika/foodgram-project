from typing import Optional, List, Iterable

from recipe.models import Recipe, Favorite, ShoppingList


def get_recipes_with_tags(tags: List[str],
                          author_id: Optional[int] = None,
                          recipe_id_seq: Optional[Iterable[int]] = None):
    query = Recipe.objects

    if recipe_id_seq is not None:
        query = query.filter(id__in=recipe_id_seq)

    if author_id is not None:
        query = query.filter(author=author_id)

    if tags:
        return query.filter(tags__in=tags)

    return query.all()


def recipe_is_favorite(user_id, recipe_id):
    return Favorite.objects.filter(
        user_id__exact=user_id, favorite_recipe_id__exact=recipe_id).exists()


def recipe_in_shop_list(user_id, recipe_id):
    return ShoppingList.objects.filter(
        user_id__exact=user_id, purchase_recipe_id__exact=recipe_id).exists()


def amount_of_purchases(user):
    counter = ShoppingList.objects.values_list('purchase_recipe_id',
                                               flat=True).filter(user_id=user)
    amount = len(counter)
    if amount == 0:
        amount = ''
    return amount
