from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class DeliveryMethod(models.Model):
    
    code         = models.SlugField(max_length=30, unique=True)  
    name         = models.CharField(max_length=50)               
    desc         = models.TextField(blank=True)
    base_price   = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    est_day_min  = models.PositiveSmallIntegerField()           
    est_day_max  = models.PositiveSmallIntegerField()
    is_active    = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]
        db_table = "delivery_method"

    def __str__(self):
        return self.name

class ShopDelivery(models.Model):
    
    shop           = models.ForeignKey("_shop_app.Shop", on_delete=models.CASCADE)
    method         = models.ForeignKey(DeliveryMethod, on_delete=models.CASCADE)
    extra_surcharge = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        db_table = "shop_delivery"
        unique_together = ("shop", "method")
        verbose_name = _("Shop delivery option")
        verbose_name_plural = _("Shop delivery options")

    def __str__(self):
        return f"{self.shop} – {self.method}"