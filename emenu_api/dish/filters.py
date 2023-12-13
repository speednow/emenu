from django_filters import rest_framework as filters

from .models import Dish


class DishFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    name__exact = filters.CharFilter(field_name="name", lookup_expr="exact")
    price__gte = filters.NumberFilter(field_name="price", lookup_expr="gte")
    price__lte = filters.NumberFilter(field_name="price", lookup_expr="lte")
    price__exact = filters.NumberFilter(field_name="price", lookup_expr="exact")
    preparation_time__gte = filters.NumberFilter(field_name="preparation_time", lookup_expr="gte")
    preparation_time__lte = filters.NumberFilter(field_name="preparation_time", lookup_expr="lte")
    preparation_time__exact = filters.NumberFilter(field_name="preparation_time", lookup_expr="exact")
    created_at__gte = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_at__lte = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    updated_at__gte = filters.DateTimeFilter(field_name="updated_at", lookup_expr="gte")
    updated_at__lte = filters.DateTimeFilter(field_name="updated_at", lookup_expr="lte")

    class Meta:
        model = Dish
        fields = [
            "is_vegetarian",
            "name",
            "name__exact",
            "price__gte",
            "price__lte",
            "price__exact",
            "preparation_time__gte",
            "preparation_time__lte",
            "preparation_time__exact",
            "created_at__gte",
            "created_at__lte",
            "updated_at__gte",
            "updated_at__lte",
        ]
