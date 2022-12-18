from datetime import datetime, date

from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.filters import IngredientFilter, RecipeFilter
from api.pagination import StandartProjectPagination
from api.permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly
from api.serializers import (
    ViewRecipeSerializer, IngredientSerializer,
    RecipeCreateSerializer, RecipeSerializer,
    ShoppingListSerializer, TagSerializer
)
from recipes.models import (FavoriteRecipe, Ingredient, IngredientList, Recipe,
                            ShoppingList, Tag)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (IngredientFilter,)
    search_fields = ('^name',)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorOrReadOnly,)
    pagination_class = StandartProjectPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return RecipeSerializer
        return RecipeCreateSerializer

    @action(
        methods=('POST', 'DELETE'),
        detail=True,
        url_path='favorite',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def add_del_to_favorite(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            try:
                fav_recipe = FavoriteRecipe.objects.create(
                        author=user,
                        recipe=recipe
                )
                serializer = ViewRecipeSerializer(recipe)
                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                        data=f'{e}',
                        status=status.HTTP_400_BAD_REQUEST
                )
        try:
            fav_recipe = FavoriteRecipe.objects.get(
                author=user,
                recipe=recipe
            )
            fav_recipe.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(
                data='Избранный рецепт не найден',
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(
        methods=('POST', 'DELETE'),
        detail=True,
        url_path='shopping_cart',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def add_del_to_shopping_list(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            shopping_list = ShoppingList.objects.create(
                user=user,
                recipe=recipe
            )
            serializer = ShoppingListSerializer(shopping_list)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        shopping_list = get_object_or_404(
            ShoppingList,
            user=user,
            recipe=recipe
        )
        shopping_list.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('GET',),
        detail=False,
        url_path='download_shopping_cart',
        permission_classes=(permissions.IsAuthenticated,),
    )
    def download_shopping_list(self, request):
        user = request.user
        timestamp = datetime.now().strftime('%d%m%Y%H%M')
        if user.shopping_list.exists():
            items = (
                IngredientList.objects.filter(
                    recipe__shopping_list__user=user
                ).values(
                    'ingredient__name',
                    'ingredient__measurement_unit'
                ).annotate(amount=Sum('amount'))
            )
            result = (
                f'Foodgram - список покупок\n'
                f'Пользователь: {user.first_name} {user.last_name}\n'
                f'Дата: {date.today().strftime("%d.%m.%Y")}\n\n'
            )
            for item in items:
                result += (
                    f'{item["ingredient__name"]} '
                    f'({item["ingredient__measurement_unit"]}) - '
                    f'{item["amount"]}\n'
                )
            filename = f'{user}_{timestamp}_shopping_list.txt'
            response = HttpResponse(result, content_type='text/plain')
            response['Content-Disposition'] = (
                f'attachment; filename="{filename}"')
            return response
        return Response(status=status.HTTP_400_BAD_REQUEST)
