from django import forms
from .models import Recipe, RecipeIngredient


class RecipeForm(forms.ModelForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['group'].required = False

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'image', 'ingredients', 'cooking_time', 'tag')
        help_texts = {
            'name': 'Название рецепта',
            'text': 'Описание рецепта'
        }
        labels = {
            'ingredients': 'Ингредиенты',
        }


class RecipeIngredientsForm(forms.ModelForm):
    class Meta:
        model = RecipeIngredient
        fields = ('ingredient', 'recipe', 'amount')
