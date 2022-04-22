from django.urls import include, path
from rest_framework import routers

from .views import (IngredientViewSet, RecipeViewSet, SubscriptionListView,
                    TagViewSet, UserViewSet)

router = routers.DefaultRouter()

router.register('ingredients', IngredientViewSet, basename='ingredients')
router.register('recipes', RecipeViewSet, basename='recipes')
router.register('tags', TagViewSet, basename='tags')
router.register(r'users', UserViewSet, basename="users")

urlpatterns = [
    path('users/subscriptions/', SubscriptionListView.as_view()),
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
