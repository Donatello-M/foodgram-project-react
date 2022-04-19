from re import compile

from django.shortcuts import get_object_or_404
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from recipes.models import Favorite, Recipe, Cart, Ingredient, RecipeIngredient
from tags.models import Tag
from users.models import Follow, User


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        fields = (
            'id', 'username', 'email', 'first_name', 'last_name',
            'personal_info', 'is_subscribed', 'password',
        )
        read_only_fields = ('id',)
        model = User
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        return not user.is_anonymous and Follow.objects.filter(
            user=user, author=author.id
        ).exists()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = (
            'id', 'name', 'color', 'slug',
        )

    def validate_hex_code(self, color):
        pattern = '^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
        if not compile(pattern, color):
            raise ValidationError(
                'HEX-код должен состоять из 6 символов и начинаться с #'
            )
        return color


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = (
            'id', 'name', 'unit',
        )


class RecipeIngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredients.id')
    name = serializers.ReadOnlyField(source='ingredients.name')
    unit = serializers.ReadOnlyField(source='ingredients.unit')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id', 'name', 'unit', 'amount',
        )


class RecipeIngredientCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='ingredients.id')

    class Meta:
        model = RecipeIngredient
        fields = (
            'id', 'amount',
        )


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        many=True,
    )
    ingredients = RecipeIngredientSerializer(
        source='ingredients_recipe',
        read_only=True,
        many=True,
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)
    image = Base64ImageField(max_length=None)

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'text', 'ingredients', 'cooking_time', 'tags',
            'image', 'is_in_cart', 'is_favorited', 'author',
        )
        read_only_fields = (
            'id', 'author',
        )

    def get_is_favorited(self, recipe):
        user = self.context.get('request').user
        if (user.is_authenticated and Favorite.objects.filter(
                user=user, recipe=recipe
        ).exists()):
            return True
        return False

    def get_is_in_cart(self, recipe):
        user = self.context.get('request').user
        if (user.is_authenticated and Cart.objects.filter(
                user=user, recipe=recipe
        ).exists()):
            return True
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True,
    )
    ingredients = RecipeIngredientCreateSerializer(
        source='ingredients_recipe',
        many=True,
    )
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'name', 'text', 'ingredients',
            'cooking_time', 'tags', 'image'
        )

    def validate_name(self, name):
        if not name:
            raise serializers.ValidationError('Введите название рецепта')
        return name

    def validate_text(self, text):
        if not text:
            raise serializers.ValidationError('Добавьте описание рецепта')
        return text

    def validate_tags(self, tags):
        if (not tags) or (len(tags) != len(set(tags))):
            raise serializers.ValidationError('Теги!')
        return tags

    def validate_ingredients(self, ingredients):
        if not ingredients:
            raise serializers.ValidationError('Добавьте ингридиенты')
        unique_check = list()
        for ingredient in ingredients:
            ingredient_id = ingredient.get('ingredients').get('id')
            if ((ingredient_id not in unique_check)
                and get_object_or_404(Ingredient,
                                      id=ingredient_id)):
                unique_check.append(ingredient_id)
            else:
                raise serializers.ValidationError('Проверьте id ингредиентов')
        return ingredients

    def validate_cooking_time(self, cooking_time):
        if not cooking_time:
            raise serializers.ValidationError('Укажите время приготовления')
        return cooking_time

    def create_link_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredients_id=ingredient.get('ingredients').get('id'),
                amount=ingredient.get('amount'),
            )

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients_recipe')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        self.create_link_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe

    def update(self, recipe, validated_data):
        ingredients = validated_data.pop('ingredients_recipe')
        tags = validated_data.pop('tags')
        recipe = super().update(recipe, validated_data)
        recipe.ingredients.clear()
        self.create_link_ingredients(ingredients, recipe)
        recipe.tags.set(tags)
        return recipe


class TargetSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id', 'tags', 'name', 'image', 'cooking_time',
        )


class FollowSerializer(serializers.ModelSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count'
        )

    def get_recipes_count(self, author):
        return author.recipes.count()

    def get_recipes(self, author):
        recipes = author.recipes.all()
        recipes_limit = self.context.get('request').query_params.get(
            'recipes_limit',
        )
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return TargetSerializer(recipes, many=True).data

    def get_is_subscribed(self, author):
        user = self.context.get('request').user
        return not user.is_anonymous and Follow.objects.filter(
            user=user, author=author.id
        ).exists()
