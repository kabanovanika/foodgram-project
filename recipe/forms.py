from django import forms
from .models import Recipe, RecipeIngredient, Ingredient, Tag


class RecipeIngredientsForm(forms.ModelForm):
    pass


class RecipeForm(forms.ModelForm):
    ingredients_list = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.values_list("title", flat=True).distinct(), to_field_name="title",
        widget=forms.Select())

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

# class RecipeForm(forms.ModelForm):
#     tags = forms.ModelMultipleChoiceField(
#         queryset=Tag.objects.all(), to_field_name="slug"
#     )
#     ingredients_list = forms.ModelMultipleChoiceField(
#         queryset=Ingredient.objects.values_list("title", flat=True).distinct(), to_field_name="title",
#         widget=forms.Select()
#     )
#     amount = []
#
#     class Meta:
#         model = Recipe
#         fields = (
#             "name",
#             "ingredients",
#             "tags",
#             "cooking_time",
#             "text",
#             "image",
#         )
#
#         exclude = ("tags",)
#
#     def __init__(self, data=None, *args, **kwargs):
#         if data is not None:
#             data = data.copy()
#             for tag in ("breakfast", "lunch", "dinner"):
#                 if tag in data:
#                     data.update({"tags": tag})
#             ingredients = self.get_ingredients(data)
#             for item in ingredients:
#                 data.update({"ingredients": item})
#             self.amount = self.get_amount(data)
#         super().__init__(data=data, *args, **kwargs)
#
#     def save(self, commit=True):
#         recipe_obj = super().save(commit=False)
#         recipe_obj.save()
#         ingredients_amount = self.amount
#         recipe_obj.recipe_ingredients.all().delete()
#         recipe_obj.recipe_ingredients.set(
#             [
#                 RecipeIngredient(
#                     recipe=recipe_obj, ingredient=ingredient, amount=ingredients_amount[ingredient.title]
#                 )
#                 for ingredient in self.cleaned_data["ingredients"]
#             ],
#             bulk=False,
#         )
#         self.save_m2m()
#         return recipe_obj
#
#     def get_ingredients(self, query_data):
#         """
#         Возвращает список с названием ингредиентов
#         """
#         chosen_ingredients = [
#             query_data[key]
#             for key in query_data.keys()
#             if key.startswith("nameIngredient")
#         ]
#         return chosen_ingredients
#
#     def get_amount(self, query_data):
#         """
#         Возвращает список с количеством ингредиентов
#         """
#         amount = [
#             query_data[key]
#             for key in query_data.keys()
#             if key.startswith("valueIngredient")
#         ]
#         return amount
