from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("new", views.new_recipe, name='formRecipe'),
    path("subscriptions", views.subscriptions, name='myFollow'),
    path('<str:username>/<int:recipe_id>/', views.recipe_page, name='recipe'),

]