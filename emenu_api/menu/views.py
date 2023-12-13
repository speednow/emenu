from dish.models import Dish
from django.core.cache import caches
from django.db.models import Count, Prefetch
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets
from rest_framework.response import Response

from .filters import MenuFilter
from .models import Menu
from .serializers import MenuSerializer


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MenuFilter
    ordering_fields = ["name", "dishes_count"]
    cache = caches["data"]

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        dishes_prefetch = Prefetch("dishes", queryset=Dish.objects.all())
        queryset = Menu.objects.prefetch_related(dishes_prefetch)
        if not self.request.user.is_authenticated:
            queryset = queryset.annotate(dishes_count=Count("dishes")).filter(dishes_count__gt=0)
        return queryset.order_by("-updated_at")

    def clear_menu_cache(self):
        self.cache.delete_pattern("menu_list_*")

    def get_cache_key(self, request, *args, **kwargs):
        is_authenticated = "auth" if request.user.is_authenticated else "anon"
        return f"menu_list_{is_authenticated}_{request.query_params}"

    def list(self, request, *args, **kwargs):
        cache_key = self.get_cache_key(request, *args, **kwargs)
        cache_menus = self.cache.get(cache_key)

        if not cache_menus:
            response = super().list(request, *args, **kwargs)
            self.cache.set(cache_key, response.data, timeout=180)
            return response
        return Response(cache_menus)

    def retrieve(self, request, *args, **kwargs):
        cache_key = f'menu_detail_{kwargs["pk"]}'
        cache_menu = self.cache.get(cache_key)
        if not cache_menu:
            response = super().retrieve(request, *args, **kwargs)
            self.cache.set(cache_key, response.data, timeout=180)
            return response
        return Response(cache_menu)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self.clear_menu_cache()
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self.clear_menu_cache()
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        self.clear_menu_cache()
        return response
