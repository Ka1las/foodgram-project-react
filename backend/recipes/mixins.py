class RepresentationMixin:
    def to_representation(self, instance):
        from .models import Favorite, Recipe, ShoppingCart
        from .serializers import RecipeListSerializer, ShortRecipeSerializer
        request = self.context.get('request')
        context = {'request': request}
        if isinstance(instance, Recipe):
            return RecipeListSerializer(instance, context=context).data
        elif isinstance(instance, Favorite) or isinstance(
            instance, ShoppingCart
        ):
            return ShortRecipeSerializer(instance.recipe, context=context).data
        raise Exception('Не ожидаемый тип объекта')
