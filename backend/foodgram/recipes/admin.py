from django.contrib import admin
from recipes.models import (FavoriteRecipe, Ingredient, IngredientList, Recipe,
                            ShoppingList, Tag)

EMPTY_VAL = '-empty-'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug',)
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VAL


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = EMPTY_VAL


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'author',
        'name',
        'image',
        'text',
        'cooking_time',
        'pub_date',
        'favorites_count'
    )
    search_fields = ('name',)
    list_filter = ('author', 'name', 'tags')
    empty_value_display = EMPTY_VAL

    def favorites_count(self, obj):
        return FavoriteRecipe.objects.filter(recipe=obj).count()


@admin.register(FavoriteRecipe)
class FavoriteRecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'author')
    search_fields = ('recipe', 'author')
    list_filter = ('recipe', 'author')
    empty_value_display = EMPTY_VAL


@admin.register(IngredientList)
class IngredientListAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    search_fields = ('recipe',)
    list_filter = ('recipe',)
    empty_value_display = EMPTY_VAL


@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ('id', 'recipe', 'user')
    search_fields = ('recipe', 'user')
    list_filter = ('recipe', 'user')
    empty_value_display = EMPTY_VAL
