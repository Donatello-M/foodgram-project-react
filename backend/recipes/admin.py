from django.contrib import admin

from .models import Cart, Favorite, Recipe, Ingredient, RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_count',)
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(RecipeIngredient)
admin.site.register(Cart)
admin.site.register(Favorite)
