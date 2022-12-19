from django.db import transaction
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (FavoriteRecipe, Ingredient, IngredientList, Recipe,
                            ShoppingList, Tag)
from users.models import Follow, User
from users.serializers import CustomUserSerializer


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')


class IngredientListSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all()
    )
    name = serializers.ReadOnlyField(
        source='ingredient.name'
    )
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = IngredientList
        fields = ('id', 'name', 'measurement_unit', 'amount')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug')


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavoriteRecipe
        fields = ('id', 'author', 'recipe')

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            recipe = data['recipe']
            if FavoriteRecipe.objects.filter(
                author=user,
                recipe=recipe
            ).exists():
                raise serializers.ValidationError(
                    'Рецепт уже в избранном!')
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ViewRecipeSerializer(
            instance,
            context=context
        ).data


class ViewRecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FollowListSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_subscribed'
    )
    recipes = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_recipes'
    )
    recipes_count = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_recipes_count'
    )

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )

    def get_is_subscribed(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.is_authenticated:
                return Follow.objects.filter(user=user, author=obj).exists()
        return False

    def get_recipes(self, obj):
        request = self.context.get('request')
        if request:
            rec_limit = request.query_params.get('recipes_limit')
            recipes = Recipe.objects.filter(author=obj)
            if rec_limit:
                return ViewRecipeSerializer(
                    recipes[:int(rec_limit)],
                    many=True,
                    context={'request': request}
                ).data
            return ViewRecipeSerializer(
                recipes,
                many=True,
                context={'request': request}
            ).data
        return False

    def get_recipes_count(self, obj):
        return Recipe.objects.filter(author=obj).count()


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'author'),
                message='Вы уже подписаны на данного автора.'
            )
        ]

    def to_representation(self, instance):
        request = self.context.get('request')
        return FollowListSerializer(
            instance.author,
            context={'request': request}
        ).data


class RecipeSerializer(serializers.ModelSerializer):
    tags = TagSerializer(
        read_only=True,
        many=True
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientListSerializer(
        many=True,
        read_only=True,
        source='ingredient_list'
    )
    is_favorited = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_favorited'
    )
    is_in_shopping_cart = serializers.SerializerMethodField(
        read_only=True,
        method_name='get_is_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_favorited(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.is_authenticated:
                return FavoriteRecipe.objects.filter(
                    author=user,
                    recipe__id=obj.id
                ).exists()
        return False

    def get_is_in_shopping_cart(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            if user.is_authenticated:
                return ShoppingList.objects.filter(
                    user=user,
                    recipe__id=obj.id
                ).exists()
        return False


class RecipeCreateSerializer(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientListSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def validate(self, data):
        tags = data['tags']
        if not tags:
            raise serializers.ValidationError(
                'Требуется добавить тег'
            )
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    'Тег уже добавлен'
                )
            tags_list.append(tag)
        ingredients = data['ingredients']
        if not ingredients:
            raise serializers.ValidationError(
                'Требуется добавить ингредиент'
            )
        ingredients_list = []
        for ingredient in ingredients:
            if ingredient in ingredients_list:
                raise serializers.ValidationError(
                    'Ингредиент уже добавлен'
                )
            ingredient_amount = ingredient['amount']
            if ingredient_amount >= 1:
                ingredients_list.append(ingredient)
        cooking_time = data['cooking_time']
        if cooking_time < 1:
            raise serializers.ValidationError(
                'Время готовки должно быть больше 1 мин'
            )
        return data

    @transaction.atomic
    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        recipe.tags.set(tags)
        IngredientList.objects.bulk_create(
            [
                IngredientList(
                    recipe=recipe,
                    amount=ingredient['amount'],
                    ingredient=ingredient['id'],
                ) for ingredient in ingredients
            ]
        )
        return recipe

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        if tags:
            instance.tags.set(tags)
        IngredientList.objects.filter(recipe=instance).delete()
        IngredientList.objects.bulk_create(
            [
                IngredientList(
                    recipe=instance,
                    amount=ingredient['amount'],
                    ingredient=ingredient['id'],
                ) for ingredient in ingredients
            ]
        )
        return super().update(instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        return RecipeSerializer(
            instance,
            context={'request': request}
        ).data


class ShoppingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('recipe', 'user')

    def validate(self, data):
        request = self.context.get('request')
        user = request.user
        if user.is_authenticated:
            recipe = data['recipe']
            if ShoppingList.objects.filter(
                user=user,
                recipe=recipe
            ).exists():
                return serializers.ValidationError(
                    'Рецепт уже добавлен'
                )
        return data

    def to_representation(self, instance):
        request = self.context.get('request')
        return FavoriteRecipeSerializer(
            instance.recipe,
            context={'request': request}
        ).data
