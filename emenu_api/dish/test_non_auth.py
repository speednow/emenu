from dish.models import Dish
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class DishUnauthorizedTestCase(APITestCase):
    def setUp(self):
        Dish.objects.create(name="Test Dish 1", price=10.50, description="Test Description 1", preparation_time=15, is_vegetarian=True)
        Dish.objects.create(name="Test Dish 2", price=15.00, description="Test Description 2", preparation_time=20, is_vegetarian=False)

    def test_list_dishes_unauthorized(self):
        response = self.client.get(reverse("dish-list"))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_dish_unauthorized(self):
        data = {"name": "New Dish", "price": 20.00, "description": "New Description", "preparation_time": 30, "is_vegetarian": True}
        response = self.client.post(reverse("dish-list"), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_single_dish_unauthorized(self):
        dish = Dish.objects.first()
        response = self.client.get(reverse("dish-detail", kwargs={"pk": dish.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_dish_unauthorized(self):
        dish = Dish.objects.first()
        response = self.client.delete(reverse("dish-detail", kwargs={"pk": dish.id}))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_dish_unauthorized(self):
        dish = Dish.objects.first()
        data = {"name": "Updated Dish", "price": 25.00, "description": "Updated Description", "preparation_time": 40, "is_vegetarian": False}
        response = self.client.put(reverse("dish-detail", kwargs={"pk": dish.id}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_partial_update_dish_unauthorized(self):
        dish = Dish.objects.first()
        data = {"price": 30.00}
        response = self.client.patch(reverse("dish-detail", kwargs={"pk": dish.id}), data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_dish_with_image_unauthorized(self):
        data = {"name": "Dish with Image", "price": 20.00, "description": "Description with Image", "preparation_time": 30, "is_vegetarian": True}
        response = self.client.post(reverse("dish-list"), data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_dishes_by_name_unauthorized(self):
        response = self.client.get(reverse("dish-list"), {"name__exact": "Test Dish 1"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_dishes_by_price_range_unauthorized(self):
        response = self.client.get(reverse("dish-list"), {"price__gte": 10.00, "price__lte": 15.00})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_filter_dishes_by_created_at_range_unauthorized(self):
        response = self.client.get(reverse("dish-list"), {"created_at__gte": "2023-01-01T00:00:00Z", "created_at__lte": "2023-12-31T23:59:59Z"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
