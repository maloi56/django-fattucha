from django.urls import path

from recipes.views import (AddRecipeView, RecipeInstanceView, RecipesViews,
                           like_post)

app_name = 'recipes'

urlpatterns = [
    path('', RecipesViews.as_view(), name='recipes'),
    path('filter/<slug:filter>/category/<int:category_id>/page/<int:page>/', RecipesViews.as_view(), name='recipes'),
    path('filter/<slug:filter>/page/<int:page>/', RecipesViews.as_view(), name='recipes'),
    path('add_recipe/', AddRecipeView.as_view(), name='add_recipe'),
    path('recipe/<int:recipe_id>', RecipeInstanceView.as_view(), name='recipe'),
    path('like/', like_post, name='like'),
]
