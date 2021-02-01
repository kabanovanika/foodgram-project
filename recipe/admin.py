from django_admin_listfilter_dropdown.filters import DropdownFilter

from django.apps import apps
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from recipe.models import Recipe, Ingredient, RecipeIngredient, Tag, Follow, Favorite, ShoppingList

User = get_user_model()
models = apps.get_models()

UserAdmin.list_filter = (("email", DropdownFilter), ("username", DropdownFilter))


class RecipeAdmin(admin.ModelAdmin):
    list_display = ("author", "name", "text", "image")
    list_filter = (("name", DropdownFilter),)


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("title", "dimension")
    list_filter = (("title", DropdownFilter),)


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ("recipe", "ingredient", "amount")


class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")


class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "author")


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "favorite_recipe")


class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ("user", "purchase_recipe")


admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(ShoppingList, ShoppingListAdmin)
