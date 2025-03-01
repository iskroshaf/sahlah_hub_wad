import uuid
from django.db import models

from _user_app.models import CustomUser

class Seller(CustomUser):
    seller_id = models.CharField(max_length=8, unique=True)
    is_approved = models.BooleanField(default=False)
    business_license = models.FileField(upload_to='file_business_licenses/')

    class Meta:
        db_table = "seller"
    
    def __str__(self):
        return self.username
    
    def save(self, *args, **kwargs):

        if not self.seller_id:
            random_number = str(uuid.uuid4().int)[:5]  
            self.seller_id = 'sel' + random_number 
        super().save(*args, **kwargs)


