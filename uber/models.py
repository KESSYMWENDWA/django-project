from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensures that each email is unique

    def _str_(self):
        return self.username

class Ride(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    current_location = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    ride_type = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"{self.user.username} - {self.ride_type} from {self.current_location} to {self.destination}"
    
class Payment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ride = models.ForeignKey('Ride', on_delete=models.CASCADE)
    mpesa_code = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Payment {self.id} for {self.user.username}"