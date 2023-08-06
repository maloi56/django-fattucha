from django.contrib import admin

from recipes.models import (CookingSteps, Ingredient, Likes, Recipe,
                            RecipeCategory)


@admin.register(RecipeCategory)
class EmailVerifyAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


class IngredientInline(admin.StackedInline):
    model = Ingredient


class StepsInline(admin.TabularInline):
    model = CookingSteps


class LikesInline(admin.TabularInline):
    model = Likes


@admin.register(Recipe)
class EmailVerifyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'creator', 'category')
    fields = (
        'name', 'description', 'creator', 'portion', 'time_to_cook', 'category', 'image', 'status',)
    inlines = [IngredientInline, StepsInline, LikesInline]


@admin.register(Ingredient)
class TariffAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'recipe',)
