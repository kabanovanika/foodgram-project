from django.urls import path
from . import views
# from .views import Subscription
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = (
    path('subscriptions', views.subscriptions, name='my_follow'),
    path("home", views.index, name="index"),
    path('favorites', views.favorites, name='favorites'),
    path("ingredients", views.get_ingredients),
    path("new", views.new_recipe, name='formRecipe'),
    path('<str:username>/', views.profile, name='profile'),
    path("<str:username>/follow", views.profile_follow, name="profile_follow"),
    path("purchases", views.purchases, name="purchases"),
    path('recipe/<int:recipe_id>/', views.recipe_page, name='recipe'),
    path('recipe/<int:recipe_id>/edit', views.recipe_edit, name='recipe_edit'),
)
