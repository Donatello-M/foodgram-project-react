from django.core.validators import MinValueValidator
from django.db import models

from recipes.models import Recipe


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название',
    )
    unit = models.CharField(
        max_length=200, verbose_name='Единица измерения',
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients_recipe',
    )
    ingredients = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='ingredients_recipe',
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество/Вес/Объем',
        validators=[MinValueValidator(1)],
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredients'],
                name='ingredients_recipe',
            ),
        ]
        verbose_name = 'Ингредиент в рецепте'
        verbose_name_plural = 'Ингредиенты в рецептах'
        ordering = ('recipe',)

    def __str__(self):
        return self.recipe.name
