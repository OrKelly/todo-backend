from rest_framework import status
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from core.mixins import SerializerMapMixin
from users.api.v1.serializers.users import UserSerializer
from users.models import User
from users.services.user_create import UserCreateService


class UserViewSet(RetrieveModelMixin, SerializerMapMixin, GenericViewSet):
    serializer_map = {"create": UserSerializer}
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = UserCreateService(
            validated_data=serializer.validated_data
        ).execute()
        response_serializer = self.serializer_class(user)
        return Response(
            status=status.HTTP_201_CREATED, data=response_serializer.data
        )
