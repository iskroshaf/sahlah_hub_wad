import uuid
from django.db import models
from _user_app.models import CustomUser
from django.contrib.auth.models import AbstractUser
from django.conf import settings


class Customer(CustomUser):
    customer_id = models.CharField(max_length=8, unique=True)
    def __str__(self):
        return self.username
    
    class Meta:
        db_table = "customer"
    
    def save(self, *args, **kwargs):
        if not self.customer_id:
            random_number = str(uuid.uuid4().int)[:5]  
            self.customer_id = 'cus' + random_number 
        super().save(*args, **kwargs)


class ShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='shipping_addresses')
    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    country = models.CharField(max_length=100, default="Malaysia")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "shipping_address"
    def __str__(self):
        return f"{self.address_line1}, {self.city}"