from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("recipe", views.new_recipe, name='formRecipe'),

]