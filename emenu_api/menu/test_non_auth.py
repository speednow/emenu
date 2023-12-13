from dish.models import Dish
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Menu


class UnauthenticatedMenuTestCase(APITestCase):
    def setUp(self):
        self.dish1 = Dish.objects.create(name="Test Dish 1", price=10.50, description="Test Description 1", preparation_time=15, is_vegetarian=True)
        self.dish2 = Dish.objects.create(name="Test Dish 2", price=15.00, description="Test Description 2", preparation_time=20, is_vegetarian=False)

        self.menu1 = Menu.objects.create(name="Test Menu 1", description="Test Description 1")
        self.menu1.dishes.add(self.dish1, self.dish2)
        self.menu2 = Menu.objects.create(name="Test Menu 2", description="Test Description 2")

    def test_list_menus(self):
        response = self.client.get(reverse("menu-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 11)

    def test_get_single_menu(self):
        menu = Menu.objects.first()
        response = self.client.get(reverse("menu-detail", kwargs={"pk": menu.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], menu.name)

    def test_filter_menus_by_name(self):
        response = self.client.get(reverse("menu-list"), {"name__exact": "Test Menu 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_filter_menus_by_created_at_range(self):
        response = self.client.get(reverse("menu-list"), {"created_at__gte": "2023-01-01T00:00:00Z", "created_at__lte": "2023-12-31T23:59:59Z"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 11)

    def test_filter_menus_by_updated_at_range(self):
        response = self.client.get(reverse("menu-list"), {"updated_at__gte": "2023-01-01T00:00:00Z", "updated_at__lte": "2023-12-31T23:59:59Z"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 11)

    def test_create_menu_with_dishes(self):
        data = {"name": "New Menu with Dishes", "description": "New Description", "dish_ids": [self.dish1.id, self.dish2.id]}
        response = self.client.post(reverse("menu-list"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_menu_with_dishes(self):
        menu = Menu.objects.first()
        data = {"name": "Updated Menu", "description": "Updated Description", "dish_ids": [self.dish1.id, self.dish2.id]}
        response = self.client.put(reverse("menu-detail", kwargs={"pk": menu.id}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_menu_with_dishes(self):
        menu = Menu.objects.first()
        data = {
            "description": "Updated Description",
            "dish_ids": [self.dish1.id],
        }
        response = self.client.patch(reverse("menu-detail", kwargs={"pk": menu.id}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_menu(self):
        menu = Menu.objects.first()
        response = self.client.delete(reverse("menu-detail", kwargs={"pk": menu.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_menu(self):
        data = {"name": "New Menu", "description": "New Description"}
        response = self.client.post(reverse("menu-list"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_menu(self):
        menu = Menu.objects.first()
        data = {"name": "Updated Menu", "description": "Updated Description"}
        response = self.client.put(reverse("menu-detail", kwargs={"pk": menu.id}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_menu(self):
        menu = Menu.objects.first()
        data = {"description": "Updated Description"}
        response = self.client.patch(reverse("menu-detail", kwargs={"pk": menu.id}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
