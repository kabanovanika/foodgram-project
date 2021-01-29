from recipe.models import Favorite, ShoppingList


class DomainUser:
    def __init__(self, id):
        self.id = id

    def favorites(self):
        return Favorite.objects.values_list('favorite_recipe_id', flat=True).filter(user_id=self.id)

    def shopping_list(self):
        return ShoppingList.objects.values_list('purchase_recipe_id', flat=True).filter(user_id=self.id)
