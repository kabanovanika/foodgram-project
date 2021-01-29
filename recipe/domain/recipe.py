from typing import Optional, List, Iterable

from recipe.models import Recipe


def get_recipes_with_tags(tags: List[str], author_id: Optional[int] = None,
                          recipe_id_seq: Optional[Iterable[int]] = None):
    query = Recipe.objects

    if recipe_id_seq is not None:
        query = query.filter(id__in=recipe_id_seq)

    if author_id is not None:
        query = query.filter(author=author_id)

    if tags:
        return query.filter(tags__in=tags)

    return query.all()
