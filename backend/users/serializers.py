from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Subscribe, User


class CustomUserCreateSerializer(UserCreateSerializer):

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class CustomUserSerializer(UserSerializer):

    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Subscribe.objects.filter(user=user, author=obj.id).exists()


class SubscribeSerializer(CustomUserSerializer):

    recipes = serializers.SerializerMethodField(read_only=True)
    recipes_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')

    @staticmethod
    def get_recipes_count(obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        from api.serializers import ShortRecipeSerializer
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return ShortRecipeSerializer(recipes, many=True).data

    def validate(self, data):
        request = self.context.get('request')
        author_id = data['author'].id
        follow_exists = Subscribe.objects.filter(
            user=request.user,
            author__id=author_id
        ).exists()

        if request.method == 'GET':
            if request.user.id == author_id:
                raise serializers.ValidationError(
                    'Нельзя подписаться на себя'
                )
            if follow_exists:
                raise serializers.ValidationError(
                    'Вы уже подписаны на этого пользователя'
                )

        return data

    @staticmethod
    def validate_user_subscription(subscription):
        if not subscription:
            return Response(
                {'error': 'Вы не подписаны на пользователя'},
                status=status.HTTP_400_BAD_REQUEST
            )
