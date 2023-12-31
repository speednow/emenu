from dish.models import Dish
from django.contrib.auth.models import User
from django.core.cache import caches
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Menu
from .serializers import MenuSerializer


class MenuTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")

        self.dish1 = Dish.objects.create(name="Test Dish 1", price=10.50, description="Test Description 1", preparation_time=15, is_vegetarian=True)
        self.dish2 = Dish.objects.create(name="Test Dish 2", price=15.00, description="Test Description 2", preparation_time=20, is_vegetarian=False)

        Menu.objects.create(name="Test Menu 1", description="Test Description 1")
        Menu.objects.create(name="Test Menu 2", description="Test Description 2")

    def test_create_menu_with_dishes(self):
        data = {"name": "New Menu with Dishes", "description": "New Description", "dish_ids": [self.dish1.id, self.dish2.id]}
        response = self.client.post(reverse("menu-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 13)
        new_menu = Menu.objects.get(name="New Menu with Dishes")
        self.assertEqual(new_menu.dishes.count(), 2)
        self.assertTrue(self.dish1 in new_menu.dishes.all())
        self.assertTrue(self.dish2 in new_menu.dishes.all())

    def test_update_menu_with_dishes(self):
        menu = Menu.objects.first()
        data = {"name": "Updated Menu", "description": "Updated Description", "dish_ids": [self.dish1.id, self.dish2.id]}
        response = self.client.put(reverse("menu-detail", kwargs={"pk": menu.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_menu = Menu.objects.get(pk=menu.id)
        self.assertEqual(updated_menu.name, "Updated Menu")
        self.assertEqual(updated_menu.dishes.count(), 2)
        self.assertTrue(self.dish1 in updated_menu.dishes.all())
        self.assertTrue(self.dish2 in updated_menu.dishes.all())

    def test_partial_update_menu_with_dishes(self):
        menu = Menu.objects.first()
        data = {"description": "Updated Description", "dish_ids": [self.dish1.id]}
        response = self.client.patch(reverse("menu-detail", kwargs={"pk": menu.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_menu = Menu.objects.get(pk=menu.id)
        self.assertEqual(updated_menu.description, "Updated Description")
        self.assertEqual(updated_menu.dishes.count(), 1)
        self.assertTrue(self.dish1 in updated_menu.dishes.all())

    def test_list_menus(self):
        response = self.client.get(reverse("menu-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Menu.objects.count())

    def test_list_menus_pagination(self):
        response = self.client.get(reverse("menu-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

    def test_get_single_menu(self):
        menu = Menu.objects.first()
        response = self.client.get(reverse("menu-detail", kwargs={"pk": menu.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], menu.name)

    def test_delete_menu(self):
        menu = Menu.objects.first()
        response = self.client.delete(reverse("menu-detail", kwargs={"pk": menu.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Menu.objects.count(), 11)

    def test_create_menu(self):
        data = {"name": "New Menu", "description": "New Description"}
        response = self.client.post(reverse("menu-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 13)
        self.assertEqual(Menu.objects.last().name, "New Menu")

    def test_update_menu(self):
        menu = Menu.objects.first()
        data = {"name": "Updated Menu", "description": "Updated Description"}
        response = self.client.put(reverse("menu-detail", kwargs={"pk": menu.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_menu = Menu.objects.get(pk=menu.id)
        self.assertEqual(updated_menu.name, "Updated Menu")

    def test_partial_update_menu(self):
        menu = Menu.objects.first()
        data = {"description": "Updated Description"}
        response = self.client.patch(reverse("menu-detail", kwargs={"pk": menu.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_menu = Menu.objects.get(pk=menu.id)
        self.assertEqual(updated_menu.description, "Updated Description")

    def test_filter_menus_by_name(self):
        response = self.client.get(reverse("menu-list"), {"name__exact": "Test Menu 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Test Menu 1")

    def test_filter_menus_by_created_at_range(self):
        response = self.client.get(reverse("menu-list"), {"created_at__gte": "2023-01-01T00:00:00Z", "created_at__lte": "2023-12-12T11:59:59Z"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_menus_by_created_at_range_pagination(self):
        start_date = "2023-01-01T00:00:00Z"
        end_date = "2024-01-07T11:59:59Z"

        filtered_count = Menu.objects.filter(created_at__gte=start_date, created_at__lte=end_date).count()
        response = self.client.get(reverse("menu-list"), {"created_at__gte": start_date, "created_at__lte": end_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], filtered_count)

    def test_filter_menus_by_updated_at_range(self):
        response = self.client.get(reverse("menu-list"), {"updated_at__gte": "2023-01-01T00:00:00Z", "updated_at__lte": "2023-12-12T11:59:59Z"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_menus_by_updated_at_range_pagination(self):
        start_date = "2023-01-01T00:00:00Z"
        end_date = "2024-01-07T11:59:59Z"

        filtered_count = Menu.objects.filter(updated_at__gte=start_date, updated_at__lte=end_date).count()
        response = self.client.get(reverse("menu-list"), {"created_at__gte": start_date, "created_at__lte": end_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], filtered_count)

    def test_dishes_count(self):
        data = {"name": "New Menu with Dishes", "description": "New Description", "dish_ids": [self.dish1.id, self.dish2.id]}
        response = self.client.post(reverse("menu-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Menu.objects.count(), 13)
        new_menu = Menu.objects.get(name="New Menu with Dishes")
        self.assertEqual(new_menu.dishes.count(), 2)
        self.assertTrue(self.dish1 in new_menu.dishes.all())
        self.assertTrue(self.dish2 in new_menu.dishes.all())

        serializer = MenuSerializer(instance=new_menu)
        self.assertEqual(serializer.data["dishes_count"], 2)

    def tearDown(self):
        caches["data"].clear()
