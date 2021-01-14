from django.urls import path
from rest_framework import routers
from . import views

# router = routers.SimpleRouter()
# router.register(r'users', UserViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("ingredients/", views.getIngredients),
    path("new", views.new_recipe, name='formRecipe'),
    path("subscriptions", views.subscriptions, name='myFollow'),
    path('<str:username>/<int:recipe_id>/', views.recipe_page, name='recipe'),
]