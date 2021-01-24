from django import forms
from .models import Recipe, RecipeIngredient, Ingredient, Tag


class RecipeForm(forms.ModelForm):
    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            for tag in ("breakfast", "lunch", "dinner"):
                if tag in data:
                    data.update({"tags": Tag.objects.get(slug=tag)})
        super().__init__(data=data, *args, **kwargs)
        self.fields['image'].required = True

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'image', 'tags', 'cooking_time')
        exclude = ('ingredients',)
        help_texts = {
            'name': 'Название рецепта',
            'text': 'Описание рецепта',
        }
        labels = {
            'name': 'Название рецепта',
            'tag': 'Теги',
            'ingredients': 'Ингредиенты',
            'cooking_time': 'Время приготовления',
        }
