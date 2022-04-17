from django.contrib import admin

from .models import Favorite, Recipe, Cart


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'favorites_count',)
    list_filter = ('name', 'author', 'tags')
    search_fields = ('name', 'author', 'tags')


admin.site.register(Cart)
admin.site.register(Favorite)
