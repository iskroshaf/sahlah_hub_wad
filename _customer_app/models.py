import uuid
from django.db import models
from _user_app.models import CustomUser
from django.contrib.auth.models import AbstractUser


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