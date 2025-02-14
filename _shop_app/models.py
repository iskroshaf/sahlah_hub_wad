from django.db import models
import uuid

class Restaurant(models.Model):
    
    RESTAURANT_STATUS_CHOICES = [
        ('A', 'Active'),
        ('I', 'Inactive'),
        ('P', 'Pending'),
    ]

    seller = models.ForeignKey('_seller_app.Seller', on_delete=models.CASCADE)
    restaurant_id = models.CharField(max_length=8,unique=True, primary_key=True)
    restaurant_name = models.CharField(max_length=50)
    restaurant_phone_number = models.CharField(max_length=15, blank=True, null=True)
    restaurant_logo = models.ImageField(upload_to='media_photos/', blank=True, null=True)
    restaurant_bg_photo = models.ImageField(upload_to='media_photos/', blank=True, null=True)
    restaurant_status = models.CharField(max_length=1,choices=RESTAURANT_STATUS_CHOICES, default='P')
    restaurant_desc = models.TextField(max_length=250,blank=True,null=True)
    restaurant_category = models.CharField(max_length=50,blank=True,null=True)
    
    restaurant_rating = models.DecimalField(max_digits=2,decimal_places=1,default=0.0)
    restaurant_delivery_fee = models.DecimalField(max_digits=10, decimal_places=2 , default= 0.00)

    class Meta:
        db_table = "restaurant"

    def __str__(self):
        return self.restaurant_name
    
    
    def save(self, *args, **kwargs):
        if not self.restaurant_id:
            random_number = str(uuid.uuid4().int)[:4]
            self.restaurant_id = 'rest' + random_number 
        super().save(*args, **kwargs)
