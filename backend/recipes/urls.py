from django.urls import include, path
from rest_framework import routers

from .views import IngredientViewSet, RecipeViewSet

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')

urlpatterns = [
    path('', include(router.urls)),
]
