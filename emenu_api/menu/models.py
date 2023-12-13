from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    dishes = models.ManyToManyField("dish.Dish")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
