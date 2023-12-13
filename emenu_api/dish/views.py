from dish.models import Dish
from django.core.cache import caches
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.response import Response

from .filters import DishFilter
from .serializers import DishSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = DishFilter
    ordering_fields = ["name", "price", "preparation_time"]
    cache = caches["data"]

    def get_permissions(self):
        return [permissions.IsAuthenticated()]

    def get_cache_key(self, request, *args, **kwargs):
        return f"dish_list_{request.query_params}"

    def list(self, request, *args, **kwargs):
        cache_key = self.get_cache_key(request, *args, **kwargs)
        cache_dishes = self.cache.get(cache_key)

        if not cache_dishes:
            response = super().list(request, *args, **kwargs)
            self.cache.set(cache_key, response.data, timeout=180)  # Cachuje na 3 minuty
            return response
        return Response(cache_dishes)

    def retrieve(self, request, *args, **kwargs):
        cache_key = f'dish_detail_{kwargs["pk"]}'
        cache_dish = self.cache.get(cache_key)
        if not cache_dish:
            response = super().retrieve(request, *args, **kwargs)
            self.cache.set(cache_key, response.data, timeout=180)
            return response
        return Response(cache_dish)

    def clear_dish_cache(self):
        self.cache.delete_pattern("dish_list_*")

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.clear_dish_cache()
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.clear_dish_cache()
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        self.clear_dish_cache()
        return response
