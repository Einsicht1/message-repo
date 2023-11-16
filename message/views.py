from django.core.cache import caches
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, CreateModelMixin
from rest_framework.response import Response

from .models import Message
from .serializers import MessageSerializer


class MessageAPIView(
    GenericAPIView,
    CreateModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    cache = caches['default']
    base_cache_key = "message_{id}"

    def get(self, request, *args, **kwargs):
        obj = self.cache.get_or_set(
            key=self.get_cache_key(kwargs['pk']),
            default=self.get_object(),
            timeout=60
        )
        serializer = self.get_serializer(obj)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def perform_update(self, serializer):
        serializer.save()
        key = self.get_cache_key(serializer.instance.id)
        self.cache.delete(key)

    def perform_destroy(self, instance):
        key = self.get_cache_key(instance.id)
        instance.delete()
        self.cache.delete(key)

    def get_cache_key(self, id: int):
        return f"{self.base_cache_key.format(id=id)}"
