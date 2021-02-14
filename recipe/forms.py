from django import forms
from django.forms import ImageField
from django.forms.widgets import ClearableFileInput
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _

from .domain.recipe import EVERY_TAG
from .models import Recipe, Tag


class MyClearableFileInput(ClearableFileInput):
    initial_text = 'Текущее фото'
    input_text = 'Изменить'


class RecipeForm(forms.ModelForm):
    image = ImageField(required=True, widget=MyClearableFileInput)

    def __init__(self, data=None, *args, **kwargs):
        if data is not None:
            data = data.copy()
            for tag in EVERY_TAG:
                if tag in data:
                    data.update(
                        {'tags': get_object_or_404(Tag, slug__exact=tag)})
        super().__init__(data=data, *args, **kwargs)
        self.fields['image'].required = True

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'image', 'tags', 'ingredients', 'cooking_time')
        exclude = ('ingredients', )
        help_texts = {
            'name': 'Название рецепта',
            'text': 'Описание рецепта',
        }
        labels = {
            'name': 'Название рецепта',
            'text': 'Описание рецепта',
            'tag': 'Теги',
            'ingredients': 'Ингредиенты',
            'cooking_time': 'Время приготовления',
        }
