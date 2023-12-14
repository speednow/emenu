from dish.models import Dish
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken


class DishTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.token = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token.access_token}")

        Dish.objects.create(name="Test Dish 1", price=10.50, description="Test Description 1", preparation_time=15, is_vegetarian=True)
        Dish.objects.create(name="Test Dish 2", price=15.00, description="Test Description 2", preparation_time=20, is_vegetarian=False)

    def test_list_dishes_pagination(self):
        response = self.client.get(reverse("dish-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)

    def test_list_dishes(self):
        response = self.client.get(reverse("dish-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], Dish.objects.count())

    def test_create_dish(self):
        data = {"name": "New Dish", "price": 20.00, "description": "New Description", "preparation_time": 30, "is_vegetarian": True}
        response = self.client.post(reverse("dish-list"), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Dish.objects.count(), 26)
        self.assertEqual(Dish.objects.first().name, "New Dish")

    def test_get_single_dish(self):
        dish = Dish.objects.first()
        response = self.client.get(reverse("dish-detail", kwargs={"pk": dish.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], dish.name)

    def test_delete_dish(self):
        dish = Dish.objects.first()
        response = self.client.delete(reverse("dish-detail", kwargs={"pk": dish.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Dish.objects.count(), 24)

    def test_update_dish(self):
        dish = Dish.objects.first()
        data = {"name": "Updated Dish", "price": 25.00, "description": "Updated Description", "preparation_time": 40, "is_vegetarian": False}
        response = self.client.put(reverse("dish-detail", kwargs={"pk": dish.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_dish = Dish.objects.get(pk=dish.id)
        self.assertEqual(updated_dish.name, "Updated Dish")

    def test_partial_update_dish(self):
        dish = Dish.objects.first()
        data = {"price": 30.00}
        response = self.client.patch(reverse("dish-detail", kwargs={"pk": dish.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_dish = Dish.objects.get(pk=dish.id)
        self.assertEqual(updated_dish.price, 30.00)

    def test_create_dish_with_image(self):
        image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
        data = {"name": "Dish with Image", "price": 20.00, "description": "Description with Image", "preparation_time": 30, "is_vegetarian": True, "image": image}
        response = self.client.post(reverse("dish-list"), data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Dish.objects.filter(name="Dish with Image").exists())
        Dish.objects.filter(name="Dish with Image").delete()

    def test_filter_dishes_by_name(self):
        response = self.client.get(reverse("dish-list"), {"name__exact": "Test Dish 1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Test Dish 1")

    def test_filter_dishes_by_price_range(self):
        response = self.client.get(reverse("dish-list"), {"price__gte": 10.00, "price__lte": 15.00})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)

    def test_filter_dishes_by_created_at_range(self):
        response = self.client.get(reverse("dish-list"), {"created_at__gte": "2023-01-01T00:00:00Z", "created_at__lte": "2023-12-12T11:59:59Z"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 7)

    def test_filter_dishes_by_created_at_range_pagination(self):
        start_date = "2023-01-01T00:00:00Z"
        end_date = "2024-01-07T11:59:59Z"

        filtered_count = Dish.objects.filter(created_at__gte=start_date, created_at__lte=end_date).count()
        response = self.client.get(reverse("dish-list"), {"created_at__gte": start_date, "created_at__lte": end_date})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], filtered_count)
