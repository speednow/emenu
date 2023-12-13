import os
import time
from datetime import timedelta
from smtplib import SMTPException

from celery import shared_task
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.utils import timezone

from .models import Dish


@shared_task
def send_dish_report():
    start_of_yesterday = timezone.now() - timedelta(days=1)
    start_of_yesterday = start_of_yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_yesterday = start_of_yesterday + timedelta(days=1)

    modified_dishes = Dish.objects.filter(updated_at__gte=start_of_yesterday, updated_at__lt=end_of_yesterday)

    def dish_details(dish):
        return (
            f"- {dish.name}, Opis: {dish.description}, Cena: {dish.price}, "
            f"Czas przygotowania: {dish.preparation_time} min, "
            f"Wegetariańskie: {'Tak' if dish.is_vegetarian else 'Nie'}, "
            f"Zdjęcie: {dish.image.url if dish.image else 'Brak'}"
        )

    email_subject = f"Przepisy z dnia {start_of_yesterday.strftime('%Y-%m-%d')}"
    email_message = f"Przepisy z dnia {start_of_yesterday.strftime('%Y-%m-%d')}:\n\nOstatnio zmodyfikowane przepisy:\n" + "\n".join(
        [dish_details(dish) for dish in modified_dishes]
    )

    users = User.objects.filter(email__isnull=False)
    for user in users:
        attempts = 3
        while attempts > 0:
            try:
                send_mail(
                    email_subject,
                    email_message,
                    os.getenv("EMAIL_HOST_USER"),
                    [user.email],
                    fail_silently=False,
                )
                break
            except SMTPException as e:
                attempts -= 1
                time.sleep(3)
                if attempts == 0:
                    raise e
