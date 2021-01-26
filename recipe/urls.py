from django.urls import path
from . import views
# from .views import Subscription
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    # path('subscriptions', views.subscriptions, name='my_follow'),
    path('subscriptions', views.Subscriptions.as_view(), name='my_follow'),
    path('subscriptions/<int:author>', views.Subscriptions.as_view(), name='my_follow_delete'),
    path("follow", views.profile_follow, name="profile_follow"),
    path("home", views.index, name="index"),
    path('favorites', views.Favorites.as_view(), name='favorites'),
    path('favorites/<int:recipe_id>', views.Favorites.as_view(), name='favorites'),
    path('favorite-recipes', views.favorite_recipes, name='favorite_recipes'),
    path("ingredients", views.get_ingredients),
    path("new", views.new_recipe, name='formRecipe'),
    path("purchases", views.purchases, name="purchases"),
    path('recipe/<int:recipe_id>/', views.recipe_page, name='recipe'),
    path('recipe/<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
    path('<str:username>/', views.profile, name='profile'),
)
