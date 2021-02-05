from django.urls import path

from . import views

urlpatterns = (
    path('subscriptions/', views.Subscriptions.as_view(), name='my_follow'),
    path('subscriptions/<int:author>/',
         views.Subscriptions.as_view(),
         name='my_follow_delete'),
    path('follow/', views.profile_follow, name='profile_follow'),
    path('home/', views.index, name='index'),
    path('favorites', views.Favorites.as_view(), name='favorites'),
    path('favorites/<int:recipe_id>/',
         views.Favorites.as_view(),
         name='favorites'),
    path('favorite-recipes/', views.favorite_recipes, name='favorite_recipes'),
    path('ingredients', views.get_ingredients, name='get_ingredients'),
    path('download/', views.shop_list_file, name='download'),
    path('new/', views.new_recipe, name='formRecipe'),
    path('purchases', views.Purchases.as_view(), name='purchases'),
    path('purchases/<int:recipe_id>/',
         views.Purchases.as_view(),
         name='purchases'),
    path('purchases-list/', views.purchases_list, name='purchases-list'),
    path('recipe/<int:recipe_id>/', views.recipe_page, name='recipe'),
    path('recipe/<int:recipe_id>/edit/', views.recipe_edit,
         name='recipe_edit'),
    path('foodgram-page/', views.page_in_dev, name='foodgram'),
    path('about-author/', views.page_in_dev, name='about_author'),
    path('technologies-page/', views.page_in_dev, name='technologies'),
    path('<str:username>/', views.profile, name='profile'),
)
