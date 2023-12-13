from django_filters import rest_framework as filters

from .models import Menu


class MenuFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr="icontains")
    name__exact = filters.CharFilter(field_name="name", lookup_expr="exact")
    created_at__exact = filters.DateTimeFilter(field_name="created_at", lookup_expr="exact")
    created_at__gte = filters.DateTimeFilter(field_name="created_at", lookup_expr="gte")
    created_at__lte = filters.DateTimeFilter(field_name="created_at", lookup_expr="lte")
    updated_at__exact = filters.DateTimeFilter(field_name="updated_at", lookup_expr="exact")
    updated_at__gte = filters.DateTimeFilter(field_name="updated_at", lookup_expr="gte")
    updated_at__lte = filters.DateTimeFilter(field_name="updated_at", lookup_expr="lte")

    class Meta:
        model = Menu
        fields = [
            "name",
            "name__exact",
            "created_at__exact",
            "created_at__gte",
            "created_at__lte",
            "updated_at__exact",
            "updated_at__gte",
            "updated_at__lte",
        ]
