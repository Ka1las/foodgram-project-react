from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

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
        from recipes.serializers import ShortRecipeSerializer
        request = self.context.get('request')
        recipes = obj.recipes.all()
        recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return ShortRecipeSerializer(recipes, many=True).data


class SubscribingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscribe
        fields = ('user', 'author')

    def validate(self, data):
        request = self.context.get('request')
        author_id = data['author']
        user_id = data['user']
        subscription = Subscribe.objects.filter(
            user=request.user, author=author_id
        )
        if self.context.get('request').method == 'POST':
            if user_id == author_id:
                raise serializers.ValidationError({
                    'errors': '???? ???? ???????????? ?????????????????????? ???? ???????????? ????????!'
                })
            elif subscription.exists():
                raise serializers.ValidationError({
                    'errors': '???? ?????? ?????????????????? ???? ????????????????????????'
                })
        elif not subscription.exists():
            raise serializers.ValidationError({
                'errors': '???? ???? ?????????????????? ???? ????????????????????????'
            })
        return data

    def to_representation(self, instance):
        return SubscribeSerializer(
            instance.author,
            context={'request': self.context.get('request')}
        ).data
