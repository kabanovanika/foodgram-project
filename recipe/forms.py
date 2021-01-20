from django import forms
from .models import Recipe, RecipeIngredient, Ingredient, Tag


class RecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = True

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'image', 'cooking_time')
        exclude = ('tag', 'ingredients')
        help_texts = {
            'name': 'Название рецепта',
            'text': 'Описание рецепта',
        }
        labels = {
            'name': 'Название рецепта',
            # 'tag': 'Теги',
            'ingredients': 'Ингредиенты',
            'cooking_time': 'Время приготовления',
        }
