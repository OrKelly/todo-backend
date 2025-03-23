from rest_framework import serializers


class SerializerMapMixin:
    serializer_map: dict[str, serializers.Serializer] = {}

    def get_serializer_class(self):
        if self.action in self.serializer_map:
            return self.serializer_map[self.action]
        return super().get_serializer_class()
