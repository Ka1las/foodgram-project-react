from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from commom.pagination import LimitFieldPagination

from .models import Subscribe, User
from .serializers import (CustomUserSerializer, SubscribeSerializer,
                          SubscribingSerializer)


class CustomUserViewSet(UserViewSet):

    queryset = User.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = LimitFieldPagination

    @action(
        detail=True,
        methods=['POST'],
        permission_classes=[IsAuthenticated]
    )
    def subscribe(self, request, id):
        data = {'user': request.user.id, 'author': id}
        serializer = SubscribingSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        model_obj = get_object_or_404(Subscribe, user=user, author=author)
        model_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=False,
        methods=['GET'],
        permission_classes=[IsAuthenticated],
        url_path='subscriptions'
    )
    def subscriptions(self, request):
        current_user = request.user
        followed_list = User.objects.filter(subscribing__user=current_user)
        authors = self.paginate_queryset(followed_list)
        serializer = SubscribeSerializer(
            authors,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
