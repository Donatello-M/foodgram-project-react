from django.contrib import admin

from .models import Ingredient, RecipeIngredient


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'unit',
    )
    list_filter = ('name',)
    search_fields = ('name',)


admin.site.register(RecipeIngredient)
