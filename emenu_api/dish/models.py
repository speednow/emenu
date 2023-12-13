import os
from datetime import datetime

from django.db import models
from django.dispatch import receiver
from storages.backends.azure_storage import AzureStorage


class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    preparation_time = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_vegetarian = models.BooleanField(default=False)
    image = models.FileField(upload_to="dish_images/", null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.image:
            ext = self.image.name.split(".")[-1]
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            new_name = f"dish_{timestamp}.{ext}"
            self.image.name = new_name

        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-updated_at"]


@receiver(models.signals.post_delete, sender=Dish)
def delete_file(sender, instance, **kwargs):
    if instance.image:
        azure_storage = AzureStorage(account_name=os.getenv("AZURE_ACCOUNT_NAME"), account_key=os.getenv("AZURE_ACCOUNT_KEY"))
        azure_storage.delete(instance.image.name)
