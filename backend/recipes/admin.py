from django.contrib import admin

from .models import (Favorite, Ingredient, IngredientAmount, Recipe,
                     ShoppingCart, Tag)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    empty_value_display = '-пусто-'


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = '-пусто-'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'amount_favorites',
                    'amount_tags', 'amount_ingredients')
    list_filter = ('author', 'name', 'tags')
    search_fields = ('name',)
    empty_value_display = '-пусто-'

    @staticmethod
    @admin.action(description='Количество подписчиков')
    def amount_favorites(obj):
        return obj.favorites.count()

    @staticmethod
    @admin.action(description='Теги')
    def amount_tags(obj):
        return '\n'.join([i[0] for i in obj.tags.values_list('name')])

    @staticmethod
    @admin.action(description='Ингридиенты')
    def amount_ingredients(obj):
        return '\n'.join([i[0] for i in obj.ingredients.values_list('name')])


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'ingredient', 'recipe', 'amount')
    empty_value_display = '-пусто-'


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '-пусто-'


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = '-пусто-'
