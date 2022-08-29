from accessify import private
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from commom.pagination import LimitFieldPagination
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)

from .filters import IngredientSearchFilter, RecipeFilter
from .permissions import IsAuthorOrReadOnly
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          RecipeListSerializer, RecipeSerializer,
                          ShoppingCartSerializer, TagSerializer)


class TagsViewSet(ReadOnlyModelViewSet):

    queryset = Tag.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = TagSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):

    queryset = Ingredient.objects.all()
    permission_classes = (AllowAny, )
    serializer_class = IngredientSerializer
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)


class RecipeViewSet(ModelViewSet):

    queryset = Recipe.objects.all()
    permission_classes = [IsAuthorOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RecipeFilter
    pagination_class = LimitFieldPagination

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RecipeListSerializer
        return RecipeSerializer

    @private
    @staticmethod
    def post_method_for_actions(request, pk, serializers):
        data = {'user': request.user.id, 'recipe': pk}
        serializer = serializers(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @private
    @staticmethod
    def delete_method_for_actions(request, pk, model):
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)
        model_obj = get_object_or_404(model, user=user, recipe=recipe)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=FavoriteSerializer)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=Favorite)

    @action(detail=True, methods=['POST'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        return self.post_method_for_actions(
            request=request, pk=pk, serializers=ShoppingCartSerializer)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        return self.delete_method_for_actions(
            request=request, pk=pk, model=ShoppingCart)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        cur_user = request.user
        shop_list = {}
        ingredients = IngredientAmount.objects.filter(
            recipe__carts__user=cur_user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(Sum('amount'))
        for ingredient in ingredients:
            amount = ingredient['amount__sum']
            name = ingredient['ingredient__name']
            measurement_unit = ingredient['ingredient__measurement_unit']
            shop_list[name] = {
                'amount': amount,
                'measurement_unit': measurement_unit
            }
        out_list = ['Project\n\n']
        for ingr, value in shop_list.items():
            out_list.append(
                f" {ingr} - {value['amount']} "
                f"{value['measurement_unit']}\n"
            )
        response = HttpResponse(out_list, {
            'Content-Type': 'text/plain',
            'Content-Disposition': 'attachment; filename="out_list.txt"',
        })
        return response
