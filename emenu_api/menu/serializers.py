from dish.models import Dish
from dish.serializers import DishSerializer
from rest_framework import serializers

from .models import Menu
from .utils import dishes_count


class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True, read_only=True)
    dish_ids = serializers.PrimaryKeyRelatedField(many=True, write_only=True, queryset=Dish.objects.all(), source="dishes")
    dishes_count = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = ["id", "name", "description", "created_at", "updated_at", "dishes", "dish_ids", "dishes_count"]

    def get_dishes_count(self, obj):
        return dishes_count(obj)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.description = validated_data.get("description", instance.description)
        if "dishes" in validated_data:
            instance.dishes.set(validated_data["dishes"])
        instance.save()
        return instance


""" Alternative - if we want to create not existing dishes with Menu POST request
class MenuSerializer(serializers.ModelSerializer):
    dishes = DishSerializer(many=True)

    class Meta:
        model = Menu
        fields = ["id", "name", "description", "created_at", "updated_at", "dishes"]

    def create(self, validated_data):
        dishes_data = validated_data.pop('dishes', [])
        menu = Menu.objects.create(**validated_data)
        for dish_data in dishes_data:
            dish, created = Dish.objects.get_or_create(**dish_data)
            menu.dishes.add(dish)
        return menu

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.save()

        dishes_data = validated_data.get('dishes', [])
        for dish_data in dishes_data:
            dish, created = Dish.objects.get_or_create(**dish_data)
            instance.dishes.add(dish)

        # Optionak: Delete dishes that are not in request
        current_dish_ids = [dish['id'] for dish in dishes_data if 'id' in dish]
        for dish in instance.dishes.all():
            if dish.id not in current_dish_ids:
                instance.dishes.remove(dish)

        return instance

"""
