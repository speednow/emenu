from dish.models import Dish
from django.core.cache import caches
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
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
            self.cache.set(cache_key, response.data)
            return response
        return Response(cache_dishes)

    def retrieve(self, request, *args, **kwargs):
        cache_key = f'dish_detail_{kwargs["pk"]}'
        cache_dish = self.cache.get(cache_key)
        if not cache_dish:
            response = super().retrieve(request, *args, **kwargs)
            self.cache.set(cache_key, response.data)
            return response
        return Response(cache_dish)

    def clear_cache(self, dish_id):
        dish_detail_key = f"dish_detail_{dish_id}"
        cache_patterns = [
            "dish_list_*",
            "menu_list_*",
            "menu_detail_*",
        ]  # if you want to optimise menu_detail you can take dish_id, where dish in mensu exists nd clean only few details
        with transaction.atomic():
            for pattern in cache_patterns:
                self.cache.delete_pattern(pattern)

            detail_to_delete = self.cache.get(dish_detail_key)
            if detail_to_delete:
                self.cache.delete(dish_detail_key)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.clear_cache(response.data.get("id"))
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.clear_cache(response.data.get("id"))
        return response

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id

        try:
            response = super().destroy(request, *args, **kwargs)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        self.clear_cache(instance_id)

        return response
